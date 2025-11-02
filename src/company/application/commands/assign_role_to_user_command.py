from dataclasses import dataclass
from typing import Optional, Dict

from src.company.domain.entities.company_user import CompanyUser
from src.company.domain.enums import CompanyUserRole
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.company.domain.infrastructure.company_user_repository_interface import (
    CompanyUserRepositoryInterface
)
from src.company.domain.exceptions.company_exceptions import CompanyValidationError, CompanyNotFoundError
from src.shared.application.command_bus import Command, CommandHandler
from src.user.domain.value_objects.UserId import UserId


@dataclass
class AssignRoleToUserCommand(Command):
    """Command to assign a role to a company user"""
    company_id: CompanyId
    user_id: UserId
    role: CompanyUserRole
    permissions: Optional[Dict[str, bool]] = None


class AssignRoleToUserCommandHandler(CommandHandler):
    """Handler for assigning a role to a company user"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def execute(self, command: AssignRoleToUserCommand) -> None:
        """Execute the command - NO return value"""
        company_id = command.company_id
        user_id = command.user_id

        # Find CompanyUser
        company_user = self.repository.get_by_company_and_user(company_id, user_id)
        if not company_user:
            raise CompanyNotFoundError(
                f"Company user with user_id {user_id} not found for company {company_id}"
            )

        # Get permissions
        if command.permissions:
            permissions = CompanyUserPermissions.from_dict(command.permissions)
        else:
            # Use defaults based on role
            if command.role == CompanyUserRole.ADMIN:
                permissions = CompanyUserPermissions.default_for_admin()
            elif command.role == CompanyUserRole.RECRUITER:
                permissions = CompanyUserPermissions.default_for_recruiter()
            else:  # VIEWER
                permissions = CompanyUserPermissions.default_for_viewer()

        # Update company user (mutable entity, no need to return)
        company_user.update(role=command.role, permissions=permissions)

        # Save updated entity
        self.repository.save(company_user)

