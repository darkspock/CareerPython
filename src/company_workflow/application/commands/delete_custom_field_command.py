from dataclasses import dataclass

from src.company_workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteCustomFieldCommand(Command):
    """Command to delete a custom field"""
    id: str


class DeleteCustomFieldCommandHandler(CommandHandler[DeleteCustomFieldCommand]):
    """Handler for deleting a custom field"""

    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteCustomFieldCommand) -> None:
        """Handle the delete custom field command"""
        custom_field_id = CustomFieldId.from_string(command.id)
        custom_field = self._repository.get_by_id(custom_field_id)

        if not custom_field:
            raise ValueError(f"Custom field with ID {command.id} not found")

        self._repository.delete(custom_field_id)
