from dataclasses import dataclass

from src.company.domain.value_objects import CompanyId
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class DeleteCompanyCommand(Command):
    """Command to delete a company (soft delete)"""
    id: CompanyId


class DeleteCompanyCommandHandler(CommandHandler[DeleteCompanyCommand]):
    """Handler for deleting a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteCompanyCommand) -> None:
        """Execute the command - NO return value"""
        company_id = command.id
        company = self.repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.id} not found")

        # Delete using entity method (mutates state)
        company.delete()

        # Persist (soft delete)
        self.repository.save(company)
