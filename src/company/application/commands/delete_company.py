from dataclasses import dataclass

from src.company.domain.exceptions import CompanyNotFoundException
from src.company.infrastructure.repositories.company_repository import CompanyRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class DeleteCompanyCommand(Command):
    company_id: str


class DeleteCompanyCommandHandler(CommandHandler[DeleteCompanyCommand]):
    def __init__(self, company_repository: CompanyRepositoryInterface):
        self.company_repository = company_repository

    def execute(self, command: DeleteCompanyCommand) -> None:
        company = self.company_repository.get_by_id(command.company_id)
        if not company:
            raise CompanyNotFoundException(f"Company with id {command.company_id} not found")

        # Business rule: Only rejected and inactive companies can be deleted
        from src.company.domain.enums.company_status import CompanyStatusEnum
        if company.status not in [CompanyStatusEnum.REJECTED, CompanyStatusEnum.INACTIVE]:
            raise ValueError("Only rejected or inactive companies can be deleted")

        self.company_repository.delete(command.company_id)
