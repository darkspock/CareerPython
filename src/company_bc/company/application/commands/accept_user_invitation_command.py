from dataclasses import dataclass
from typing import Optional

from src.auth_bc.user.domain.entities.user import User
from src.auth_bc.user.domain.repositories.user_repository_interface import UserRepositoryInterface
from src.auth_bc.user.domain.services.password_service import PasswordService
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.company_bc.company.domain.entities.company_user import CompanyUser
from src.company_bc.company.domain.enums import CompanyUserRole
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.company_bc.company.domain.infrastructure.company_user_invitation_repository_interface import (
    CompanyUserInvitationRepositoryInterface
)
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import (
    CompanyUserRepositoryInterface
)
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId as CompanyUserEntityId
from src.company_bc.company.domain.value_objects.invitation_token import InvitationToken
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class AcceptUserInvitationCommand(Command):
    """Command to accept a user invitation"""
    token: InvitationToken
    email: Optional[str] = None  # Required if user is new
    name: Optional[str] = None  # Required if user is new
    password: Optional[str] = None  # Required if user is new
    user_id: Optional[UserId] = None  # If user already exists


class AcceptUserInvitationCommandHandler(CommandHandler):
    """Handler for accepting a user invitation"""

    def __init__(
            self,
            invitation_repository: CompanyUserInvitationRepositoryInterface,
            company_user_repository: CompanyUserRepositoryInterface,
            user_repository: UserRepositoryInterface
    ):
        self.invitation_repository = invitation_repository
        self.company_user_repository = company_user_repository
        self.user_repository = user_repository

    def execute(self, command: AcceptUserInvitationCommand) -> None:
        """Execute the command - NO return value"""
        # Find invitation by token
        invitation = self.invitation_repository.get_by_token(command.token)

        if not invitation:
            raise CompanyValidationError("Invalid invitation token")

        # Validate invitation is not expired
        if invitation.is_expired():
            invitation.expire()
            self.invitation_repository.save(invitation)
            raise CompanyValidationError("Invitation has expired")

        # Validate invitation is pending
        if not invitation.is_pending():
            raise CompanyValidationError(f"Cannot accept invitation with status {invitation.status.value}")

        # Determine if user is new or existing
        user_id: UserId
        if command.user_id:
            # Existing user
            user_id = command.user_id
            # Verify user exists
            existing_user = self.user_repository.get_by_id(user_id)
            if not existing_user:
                raise CompanyValidationError(f"User with id {user_id} not found")
        else:
            # New user - validate required fields
            if not command.email or not command.name or not command.password:
                raise CompanyValidationError(
                    "email, name, and password are required for new users"
                )

            # Validate email matches invitation
            if command.email.lower() != invitation.email.lower():
                raise CompanyValidationError("Email does not match invitation")

            # Check if user already exists by email
            existing_user_by_email = self.user_repository.get_by_email(command.email.lower())
            if existing_user_by_email:
                # User exists but wasn't provided user_id - use existing user
                user_id = existing_user_by_email.id
            else:
                # Create new user
                # Note: We don't create Candidate, only User as per requirements
                user_id = UserId.generate()
                hashed_password = PasswordService.hash_password(command.password)

                user = User(
                    id=user_id,
                    email=command.email.lower(),
                    hashed_password=hashed_password,
                    is_active=True
                )

                self.user_repository.create(user)

        # Check if user is already a company user for this company
        existing_company_user = self.company_user_repository.get_by_company_and_user(
            invitation.company_id,
            user_id
        )
        if existing_company_user:
            raise CompanyValidationError(
                f"User {user_id} is already a member of this company"
            )

        # Create CompanyUser
        company_user_id = CompanyUserEntityId.generate()
        company_user = CompanyUser.create(
            id=company_user_id,
            company_id=invitation.company_id,
            user_id=user_id,
            role=CompanyUserRole.RECRUITER,  # Default role, can be updated later
            permissions=None  # Will use defaults from role
        )

        # Save company user
        self.company_user_repository.save(company_user)

        # Update invitation to accepted
        invitation.accept()
        self.invitation_repository.save(invitation)
