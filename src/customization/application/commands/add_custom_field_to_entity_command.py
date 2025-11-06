from dataclasses import dataclass

from src.customization.domain.entities.entity_customization import EntityCustomization
from src.customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.customization.domain.value_objects.custom_field import CustomField
from src.customization.domain.exceptions.entity_customization_not_found import EntityCustomizationNotFound
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class AddCustomFieldToEntityCommand(Command):
    """Command to add a custom field to an entity customization"""
    entity_customization_id: EntityCustomizationId
    field: CustomField


class AddCustomFieldToEntityCommandHandler(CommandHandler[AddCustomFieldToEntityCommand]):
    """Handler for adding a custom field to an entity customization"""

    def __init__(self, repository: EntityCustomizationRepositoryInterface):
        self._repository = repository

    def execute(self, command: AddCustomFieldToEntityCommand) -> None:
        """Handle the add custom field command"""
        entity_customization = self._repository.get_by_id(command.entity_customization_id)
        
        if not entity_customization:
            raise EntityCustomizationNotFound(
                f"Entity customization with ID '{command.entity_customization_id}' not found"
            )
        
        entity_customization.add_field(command.field)
        self._repository.save(entity_customization)

