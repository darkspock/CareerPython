from dataclasses import dataclass

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.framework.application.command_bus import CommandHandler, Command


@dataclass
class ActivateCompanyCommand(Command):
    """Command to activate a company"""
    id: CompanyId
    activated_by: str


class ActivateCompanyCommandHandler(CommandHandler):
    """Handler for activating a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def execute(self, command: ActivateCompanyCommand) -> None:
        """Execute the command - NO return value"""
        company_id = command.id
        company = self.repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.id} not found")

        # Activate using entity method (mutates state)
        company.activate()

        # Persist
        self.repository.save(company)
