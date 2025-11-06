from dataclasses import dataclass
from typing import Dict, Any, Optional

from src.company_workflow.domain.infrastructure.custom_field_value_repository_interface import \
    CustomFieldValueRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateCustomFieldValueCommand(Command):
    """Command to update custom field values (merge with existing)"""
    id: str
    values: Optional[Dict[str, Any]] = None  # Values to merge with existing


class UpdateCustomFieldValueCommandHandler(CommandHandler[UpdateCustomFieldValueCommand]):
    """Handler for updating custom field values"""

    def __init__(self, repository: CustomFieldValueRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateCustomFieldValueCommand) -> None:
        """Handle the update custom field value command"""
        # Get existing custom field value
        existing_value = self._repository.get_by_id(CustomFieldValueId(command.id))
        if not existing_value:
            raise ValueError(f"Custom field value with id {command.id} not found")

        # Update the values (merge with existing)
        if command.values:
            updated_value = existing_value.update_values(command.values)
            self._repository.save(updated_value)
