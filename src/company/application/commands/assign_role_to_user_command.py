from dataclasses import dataclass
from typing import Optional, Dict, List

from src.company.domain.enums import CompanyUserRole
from src.company.domain.exceptions.company_exceptions import CompanyValidationError, CompanyNotFoundError
from src.company.domain.infrastructure.company_user_repository_interface import (
    CompanyUserRepositoryInterface
)
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.company_role.domain.infrastructure.company_role_repository_interface import CompanyRoleRepositoryInterface
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.shared.application.command_bus import Command, CommandHandler
from src.user.domain.value_objects.UserId import UserId


@dataclass
class AssignRoleToUserCommand(Command):
    """Command to assign a role to a company user"""
    company_id: CompanyId
    user_id: UserId
    role: CompanyUserRole
    permissions: Optional[Dict[str, bool]] = None
    company_roles: Optional[List[str]] = None  # IDs of CompanyRole to assign


class AssignRoleToUserCommandHandler(CommandHandler):
    """Handler for assigning a role to a company user"""

    def __init__(
            self,
            repository: CompanyUserRepositoryInterface,
            company_role_repository: CompanyRoleRepositoryInterface
    ):
        self.repository = repository
        self.company_role_repository = company_role_repository

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

        # Validate and assign company roles if provided
        if command.company_roles is not None:
            # Validate that all company roles exist and belong to the company
            for role_id in command.company_roles:
                role = self.company_role_repository.get_by_id(CompanyRoleId.from_string(role_id))
                if not role:
                    raise CompanyValidationError(f"Company role {role_id} not found")
                if role.company_id != company_id:
                    raise CompanyValidationError(f"Company role {role_id} does not belong to company {company_id}")

            # Assign company roles
            self.repository.assign_company_roles(company_user.id, command.company_roles)

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
