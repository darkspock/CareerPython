from dataclasses import dataclass
from typing import Optional

from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.value_objects import CompanyId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class SuspendCompanyCommand(Command):
    """Command to suspend a company"""
    id: CompanyId
    reason: Optional[str] = None


class SuspendCompanyCommandHandler(CommandHandler[SuspendCompanyCommand]):
    """Handler for suspending a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def execute(self, command: SuspendCompanyCommand) -> None:
        """Execute the command - NO return value"""
        company_id = command.id
        company = self.repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.id} not found")

        # Suspend using entity method (returns new instance)
        suspended_company = company.suspend(reason=command.reason)

        # Persist
        self.repository.save(suspended_company)
