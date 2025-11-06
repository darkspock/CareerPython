from dataclasses import dataclass

from src.workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ReorderCustomFieldCommand(Command):
    """Command to reorder a custom field"""
    id: str
    new_order_index: int


class ReorderCustomFieldCommandHandler(CommandHandler[ReorderCustomFieldCommand]):
    """Handler for reordering a custom field"""

    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def execute(self, command: ReorderCustomFieldCommand) -> None:
        """Handle the reorder custom field command"""
        custom_field_id = CustomFieldId.from_string(command.id)
        custom_field = self._repository.get_by_id(custom_field_id)

        if not custom_field:
            raise ValueError(f"Custom field with ID {command.id} not found")

        reordered_field = custom_field.reorder(command.new_order_index)

        self._repository.save(reordered_field)
