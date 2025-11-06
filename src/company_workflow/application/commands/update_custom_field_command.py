from dataclasses import dataclass
from typing import Optional, Dict, Any

from src.company_workflow.domain.enums.field_type import FieldType
from src.company_workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateCustomFieldCommand(Command):
    """Command to update a custom field"""
    id: str
    field_name: str
    field_type: str
    field_config: Optional[Dict[str, Any]] = None


class UpdateCustomFieldCommandHandler(CommandHandler[UpdateCustomFieldCommand]):
    """Handler for updating a custom field"""

    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateCustomFieldCommand) -> None:
        """Handle the update custom field command"""
        custom_field_id = CustomFieldId.from_string(command.id)
        custom_field = self._repository.get_by_id(custom_field_id)

        if not custom_field:
            raise ValueError(f"Custom field with ID {command.id} not found")

        updated_field = custom_field.update(
            field_name=command.field_name,
            field_type=FieldType(command.field_type),
            field_config=command.field_config
        )

        self._repository.save(updated_field)
