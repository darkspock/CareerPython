from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.exceptions import CompanyNotFoundException
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class UpdateCompanyCommand(Command):
    company_id: str
    name: Optional[str] = None
    sector: Optional[str] = None
    size: Optional[int] = None
    location: Optional[str] = None
    website: Optional[str] = None
    culture: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None


class UpdateCompanyCommandHandler(CommandHandler[UpdateCompanyCommand]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def execute(self, command: UpdateCompanyCommand) -> None:
        company = self.company_repository.get_by_id(command.company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with id {command.company_id} not found")

        company.update_details(
            name=command.name,
            sector=command.sector,
            size=command.size,
            location=command.location,
            website=command.website,
            culture=command.culture,
            external_data=command.external_data
        )

        self.company_repository.save(company)
