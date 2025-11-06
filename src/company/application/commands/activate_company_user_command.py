from dataclasses import dataclass

from src.company.domain.exceptions.company_exceptions import CompanyNotFoundError
from src.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.company.domain.value_objects import CompanyUserId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class ActivateCompanyUserCommand(Command):
    """Command to activate a company user"""
    id: CompanyUserId


class ActivateCompanyUserCommandHandler(CommandHandler):
    """Handler for activating a company user"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def execute(self, command: ActivateCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        company_user_id = command.id
        company_user = self.repository.get_by_id(company_user_id)

        if not company_user:
            raise CompanyNotFoundError(f"Company user with id {command.id} not found")

        # Activate using entity method (modifies instance directly)
        company_user.activate()

        # Persist
        self.repository.save(company_user)
