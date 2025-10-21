from dataclasses import dataclass

from src.company.domain.value_objects import CompanyUserId
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError


@dataclass
class DeactivateCompanyUserCommand:
    """Command to deactivate a company user"""
    id: str


class DeactivateCompanyUserCommandHandler:
    """Handler for deactivating a company user"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def handle(self, command: DeactivateCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        company_user_id = CompanyUserId.from_string(command.id)
        company_user = self.repository.get_by_id(company_user_id)

        if not company_user:
            raise CompanyNotFoundError(f"Company user with id {command.id} not found")

        # Deactivate using entity method (returns new instance)
        deactivated_company_user = company_user.deactivate()

        # Persist
        self.repository.save(deactivated_company_user)
