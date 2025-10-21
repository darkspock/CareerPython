from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.entities.company_user import CompanyUser
from src.company.domain.enums import CompanyUserRole
from src.company.domain.value_objects import CompanyId, CompanyUserId
from src.company.domain.value_objects.company_user_permissions import CompanyUserPermissions
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyValidationError
from src.user.domain.value_objects.UserId import UserId


@dataclass
class AddCompanyUserCommand:
    """Command to add a user to a company"""
    id: str
    company_id: str
    user_id: str
    role: str
    permissions: Optional[Dict[str, bool]] = None


class AddCompanyUserCommandHandler:
    """Handler for adding a user to a company"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def handle(self, command: AddCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        # Convert role string to enum
        try:
            role = CompanyUserRole(command.role)
        except ValueError:
            raise CompanyValidationError(f"Invalid role: {command.role}")

        # Convert permissions dict to value object if provided
        permissions = None
        if command.permissions:
            permissions = CompanyUserPermissions.from_dict(command.permissions)

        # Create company user using entity factory method
        company_user = CompanyUser.create(
            id=CompanyUserId.from_string(command.id),
            company_id=CompanyId.from_string(command.company_id),
            user_id=UserId(command.user_id),
            role=role,
            permissions=permissions,
        )

        # Persist
        self.repository.save(company_user)
