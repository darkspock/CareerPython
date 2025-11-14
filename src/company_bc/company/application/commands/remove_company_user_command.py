from dataclasses import dataclass

from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.company_bc.company.domain.exceptions.company_exceptions import CompanyValidationError, CompanyNotFoundError
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import \
    CompanyUserRepositoryInterface
from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class RemoveCompanyUserCommand(Command):
    """Command to remove a user from a company"""
    company_id: CompanyId
    user_id_to_remove: UserId
    current_user_id: UserId  # For validation of no self-removal


class RemoveCompanyUserCommandHandler(CommandHandler):
    """Handler for removing a user from a company"""

    def __init__(self, repository: CompanyUserRepositoryInterface):
        self.repository = repository

    def execute(self, command: RemoveCompanyUserCommand) -> None:
        """Execute the command - NO return value"""
        # Validate that current_user_id != user_id_to_remove
        if command.current_user_id == command.user_id_to_remove:
            raise CompanyValidationError("Cannot remove yourself from the company")

        company_id = command.company_id
        user_id_to_remove = command.user_id_to_remove

        # Find CompanyUser to remove
        company_user = self.repository.get_by_company_and_user(company_id, user_id_to_remove)
        if not company_user:
            raise CompanyNotFoundError(
                f"Company user with user_id {user_id_to_remove} not found for company {company_id}"
            )

        # Validate that it's not the last admin
        admin_count = self.repository.count_admins_by_company(company_id)
        if company_user.is_admin() and admin_count <= 1:
            raise CompanyValidationError(
                "Cannot remove the last admin user. At least one admin must remain."
            )

        # Delete from repository
        self.repository.delete(company_user.id)
