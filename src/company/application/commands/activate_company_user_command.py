from dataclasses import dataclass

from src.company.domain.value_objects import CompanyUserId
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError


@dataclass
class ActivateCompanyUserCommand:
    """Command to activate a company user"""
    id: str


class ActivateCompanyUserCommandHandler:
    """Handler for activating a company user"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def handle(self, command: ActivateCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        company_user_id = CompanyUserId.from_string(command.id)
        company_user = self.repository.get_by_id(company_user_id)

        if not company_user:
            raise CompanyNotFoundError(f"Company user with id {command.id} not found")

        # Activate using entity method (returns new instance)
        activated_company_user = company_user.activate()

        # Persist
        self.repository.save(activated_company_user)
