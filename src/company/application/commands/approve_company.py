from dataclasses import dataclass
from typing import Optional

from src.company.domain.exceptions import CompanyNotFoundException
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class ApproveCompanyCommand(Command):
    company_id: str
    approved_by: str
    approval_notes: Optional[str] = None


class ApproveCompanyCommandHandler(CommandHandler[ApproveCompanyCommand]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def execute(self, command: ApproveCompanyCommand) -> None:
        company = self.company_repository.get_by_id(command.company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with id {command.company_id} not found")

        company.approve()

        self.company_repository.save(company)
