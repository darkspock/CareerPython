from dataclasses import dataclass

from src.company.domain.value_objects import CompanyUserId
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError


@dataclass
class RemoveCompanyUserCommand:
    """Command to remove a user from a company"""
    id: str


class RemoveCompanyUserCommandHandler:
    """Handler for removing a user from a company"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def handle(self, command: RemoveCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        company_user_id = CompanyUserId.from_string(command.id)
        company_user = self.repository.get_by_id(company_user_id)

        if not company_user:
            raise CompanyNotFoundError(f"Company user with id {command.id} not found")

        # Delete from repository
        self.repository.delete(company_user_id)
