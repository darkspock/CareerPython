from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.value_objects import CompanyId, CompanySettings
from src.company.domain.infrastructure.company_repository_interface import CompanyRepositoryInterface
from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.shared.application.command_bus import CommandHandler, Command


@dataclass
class UpdateCompanyCommand(Command):
    """Command to update a company"""
    id: str
    name: str
    domain: str
    logo_url: Optional[str]
    settings: Dict[str, Any]


class UpdateCompanyCommandHandler(CommandHandler):
    """Handler for updating a company"""

    def __init__(self, repository: CompanyRepositoryInterface):
        self.repository = repository

    def execute(self, command: UpdateCompanyCommand) -> None:
        """Execute the command - NO return value"""
        company_id = CompanyId.from_string(command.id)
        company = self.repository.get_by_id(company_id)

        if not company:
            raise CompanyNotFoundError(f"Company with id {command.id} not found")

        # Update using entity method (returns new instance)
        updated_company = company.update(
            name=command.name,
            domain=command.domain,
            logo_url=command.logo_url,
            settings=CompanySettings.from_dict(command.settings),
        )

        # Persist
        self.repository.save(updated_company)
