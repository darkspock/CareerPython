from dataclasses import dataclass
from typing import Optional

from src.company.domain.value_objects import CompanyId
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError


@dataclass
class SuspendCompanyCommand:
    """Command to suspend a company"""
    id: str
    reason: Optional[str] = None


class SuspendCompanyCommandHandler:
    """Handler for suspending a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def handle(self, command: SuspendCompanyCommand) -> None:
        """Execute the command - NO return value"""
        company_id = CompanyId.from_string(command.id)
        company = self.repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.id} not found")

        # Suspend using entity method (returns new instance)
        suspended_company = company.suspend(reason=command.reason)

        # Persist
        self.repository.save(suspended_company)
