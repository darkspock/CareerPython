from dataclasses import dataclass

from src.company_bc.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company_bc.company.domain.value_objects import CompanyUserId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class DeactivateCompanyUserCommand(Command):
    """Command to deactivate a company user"""
    id: CompanyUserId


class DeactivateCompanyUserCommandHandler(CommandHandler[DeactivateCompanyUserCommand]):
    """Handler for deactivating a company user"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeactivateCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        company_user = self.repository.get_by_id(command.id)

        if not company_user:
            raise CompanyNotFoundError(f"Company user with id {command.id} not found")

        # Deactivate using entity method (modifies instance directly)
        company_user.deactivate()

        # Persist
        self.repository.save(company_user)
