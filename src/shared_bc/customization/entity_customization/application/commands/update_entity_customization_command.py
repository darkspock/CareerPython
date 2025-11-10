from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from src.shared_bc.customization.entity_customization.domain.entities.entity_customization import EntityCustomization
from src.shared_bc.customization.entity_customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field import CustomField
from src.shared_bc.customization.entity_customization.domain.exceptions.entity_customization_not_found import EntityCustomizationNotFound
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateEntityCustomizationCommand(Command):
    """Command to update an entity customization"""
    id: EntityCustomizationId
    fields: Optional[List[CustomField]] = None
    validation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class UpdateEntityCustomizationCommandHandler(CommandHandler[UpdateEntityCustomizationCommand]):
    """Handler for updating an entity customization"""

    def __init__(self, repository: EntityCustomizationRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateEntityCustomizationCommand) -> None:
        """Handle the update entity customization command"""
        entity_customization = self._repository.get_by_id(command.id)
        
        if not entity_customization:
            raise EntityCustomizationNotFound(f"Entity customization with ID '{command.id}' not found")
        
        entity_customization.update(
            fields=command.fields,
            validation=command.validation,
            metadata=command.metadata
        )

        self._repository.save(entity_customization)

