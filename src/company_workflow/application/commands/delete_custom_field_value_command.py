from dataclasses import dataclass

from src.company_workflow.domain.infrastructure.custom_field_value_repository_interface import \
    CustomFieldValueRepositoryInterface
from src.company_workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteCustomFieldValueCommand(Command):
    """Command to delete a custom field value"""
    id: str


class DeleteCustomFieldValueCommandHandler(CommandHandler[DeleteCustomFieldValueCommand]):
    """Handler for deleting custom field values"""

    def __init__(self, repository: CustomFieldValueRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteCustomFieldValueCommand) -> None:
        """Handle the delete custom field value command"""
        self._repository.delete(CustomFieldValueId(command.id))
