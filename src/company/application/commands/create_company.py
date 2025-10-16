from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company.domain.entities.company import Company
from src.company.domain.value_objects.company_id import CompanyId
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler
from src.user.domain.value_objects.UserId import UserId


@dataclass
class CreateCompanyCommand(Command):
    id: CompanyId
    user_id: Optional[UserId]
    name: str
    sector: Optional[str] = None
    size: Optional[int] = None
    location: Optional[str] = None
    website: Optional[str] = None
    culture: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None


class CreateCompanyCommandHandler(CommandHandler[CreateCompanyCommand]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def execute(self, command: CreateCompanyCommand) -> None:
        company = Company.create(
            id=command.id,
            user_id=command.user_id,
            name=command.name,
            sector=command.sector,
            size=command.size,
            location=command.location,
            website=command.website,
            culture=command.culture,
            external_data=command.external_data
        )

        self.company_repository.save(company)
