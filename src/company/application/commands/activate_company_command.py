from dataclasses import dataclass

from src.company.domain.value_objects import CompanyId
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.shared.application.command_bus import CommandHandler, Command


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
        company_id = CompanyId.from_string(command.id)
        company = self.repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.id} not found")

        # Activate using entity method (returns new instance)
        activated_company = company.activate()

        # Persist
        self.repository.save(activated_company)
