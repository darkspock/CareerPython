"""Delete Role Command."""
from dataclasses import dataclass

from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company_role.domain.exceptions.role_not_found import RoleNotFound
from src.company_role.domain.infrastructure.company_role_repository_interface import CompanyRoleRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteRoleCommand(Command):
    """Command to delete a company role."""
    id: str


class DeleteRoleCommandHandler(CommandHandler[DeleteRoleCommand]):
    """Handler for deleting a company role."""

    def __init__(self, repository: CompanyRoleRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteRoleCommand) -> None:
        """Handle the delete role command."""
        role_id = CompanyRoleId.from_string(command.id)
        role = self.repository.get_by_id(role_id)

        if not role:
            raise RoleNotFound(f"Role with id {command.id} not found")

        self.repository.delete(role_id)
