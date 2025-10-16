from dataclasses import dataclass

from src.company.domain.exceptions import CompanyNotFoundException
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class ActivateCompanyCommand(Command):
    company_id: str
    activated_by: str


class ActivateCompanyCommandHandler(CommandHandler[ActivateCompanyCommand]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def execute(self, command: ActivateCompanyCommand) -> None:
        company = self.company_repository.get_by_id(command.company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with id {command.company_id} not found")

        company.activate()

        self.company_repository.save(company)
