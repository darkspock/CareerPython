"""Update Role Command."""
from dataclasses import dataclass
from typing import Optional

from src.company_bc.company_role.domain.exceptions.role_not_found import RoleNotFound
from src.company_bc.company_role.domain.infrastructure.company_role_repository_interface import \
    CompanyRoleRepositoryInterface
from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateRoleCommand(Command):
    """Command to update a company role."""
    id: CompanyRoleId
    name: str
    description: Optional[str] = None


class UpdateRoleCommandHandler(CommandHandler[UpdateRoleCommand]):
    """Handler for updating a company role."""

    def __init__(self, repository: CompanyRoleRepositoryInterface):
        self.repository = repository

    def execute(self, command: UpdateRoleCommand) -> None:
        """Handle the update role command."""
        role_id = command.id
        role = self.repository.get_by_id(role_id)

        if not role:
            raise RoleNotFound(f"Role with id {command.id} not found")

        # Check if new name conflicts with existing role
        if self.repository.exists_by_name(role.company_id, command.name, exclude_id=role_id):
            raise ValueError(f"Role with name '{command.name}' already exists for this company")

        updated_role = role.update(
            name=command.name,
            description=command.description
        )

        self.repository.save(updated_role)
