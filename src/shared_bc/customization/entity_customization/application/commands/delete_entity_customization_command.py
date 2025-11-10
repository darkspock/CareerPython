from dataclasses import dataclass

from src.shared_bc.customization.entity_customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.shared_bc.customization.entity_customization.domain.exceptions.entity_customization_not_found import EntityCustomizationNotFound
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteEntityCustomizationCommand(Command):
    """Command to delete an entity customization"""
    id: EntityCustomizationId


class DeleteEntityCustomizationCommandHandler(CommandHandler[DeleteEntityCustomizationCommand]):
    """Handler for deleting an entity customization"""

    def __init__(self, repository: EntityCustomizationRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteEntityCustomizationCommand) -> None:
        """Handle the delete entity customization command"""
        entity_customization = self._repository.get_by_id(command.id)
        
        if not entity_customization:
            raise EntityCustomizationNotFound(f"Entity customization with ID '{command.id}' not found")
        
        self._repository.delete(command.id)

