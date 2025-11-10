"""Create Role Command."""
from dataclasses import dataclass
from typing import Optional
import ulid

from src.company_role.domain.entities.company_role import CompanyRole
from src.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_role.domain.infrastructure.company_role_repository_interface import CompanyRoleRepositoryInterface
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateRoleCommand(Command):
    """Command to create a new company role."""
    id: CompanyRoleId
    company_id: str
    name: str
    description: Optional[str] = None


class CreateRoleCommandHandler(CommandHandler[CreateRoleCommand]):
    """Handler for creating a new company role."""

    def __init__(self, repository: CompanyRoleRepositoryInterface):
        self.repository = repository

    def execute(self, command: CreateRoleCommand) -> None:
        """Handle the create role command."""
        company_id = CompanyId(command.company_id)

        # Check if role name already exists for this company
        if self.repository.exists_by_name(company_id, command.name):
            raise ValueError(f"Role with name '{command.name}' already exists for this company")

        role_id = CompanyRoleId(str(ulid.new()))

        role = CompanyRole.create(
            id=role_id,
            company_id=company_id,
            name=command.name,
            description=command.description
        )

        self.repository.save(role)

        # Set the generated ID back on the command for retrieval
        # Note: This is a workaround since the command is frozen
        # In a better design, we'd use a separate result object
        object.__setattr__(command, 'id', str(role_id))
