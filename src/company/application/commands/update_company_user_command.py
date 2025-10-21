from dataclasses import dataclass
from typing import Dict

from src.company.domain.enums import CompanyUserRole
from src.company.domain.value_objects import CompanyUserId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError, CompanyValidationError


@dataclass
class UpdateCompanyUserCommand:
    """Command to update a company user"""
    id: str
    role: str
    permissions: Dict[str, bool]


class UpdateCompanyUserCommandHandler:
    """Handler for updating a company user"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def handle(self, command: UpdateCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        company_user_id = CompanyUserId.from_string(command.id)
        company_user = self.repository.get_by_id(company_user_id)

        if not company_user:
            raise CompanyNotFoundError(f"Company user with id {command.id} not found")

        # Convert role string to enum
        try:
            role = CompanyUserRole(command.role)
        except ValueError:
            raise CompanyValidationError(f"Invalid role: {command.role}")

        # Update using entity method (returns new instance)
        updated_company_user = company_user.update(
            role=role,
            permissions=CompanyUserPermissions.from_dict(command.permissions),
        )

        # Persist
        self.repository.save(updated_company_user)
