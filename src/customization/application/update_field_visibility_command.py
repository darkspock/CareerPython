from dataclasses import dataclass

from src.workflow.domain.infrastructure.field_configuration_repository_interface import FieldConfigurationRepositoryInterface
from src.workflow.domain.value_objects.field_configuration_id import FieldConfigurationId
from src.workflow.domain.enums.field_visibility import FieldVisibility
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateFieldVisibilityCommand(Command):
    """Command to update field visibility in a stage"""
    id: str
    visibility: str


class UpdateFieldVisibilityCommandHandler(CommandHandler[UpdateFieldVisibilityCommand]):
    """Handler for updating field visibility"""

    def __init__(self, repository: FieldConfigurationRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateFieldVisibilityCommand) -> None:
        """Handle the update field visibility command"""
        field_configuration_id = FieldConfigurationId.from_string(command.id)
        field_configuration = self._repository.get_by_id(field_configuration_id)

        if not field_configuration:
            raise ValueError(f"Field configuration with ID {command.id} not found")

        updated_configuration = field_configuration.update_visibility(
            visibility=FieldVisibility(command.visibility)
        )

        self._repository.save(updated_configuration)
