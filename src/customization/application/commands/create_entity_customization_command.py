from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from src.customization.domain.entities.entity_customization import EntityCustomization
from src.customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from src.customization.domain.value_objects.custom_field import CustomField
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateEntityCustomizationCommand(Command):
    """Command to create a new entity customization"""
    entity_type: EntityCustomizationTypeEnum
    entity_id: str
    fields: List[CustomField]
    id: Optional[EntityCustomizationId] = None
    validation: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None


class CreateEntityCustomizationCommandHandler(CommandHandler[CreateEntityCustomizationCommand]):
    """Handler for creating a new entity customization"""

    def __init__(self, repository: EntityCustomizationRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateEntityCustomizationCommand) -> None:
        """Handle the create entity customization command
        
        If a customization already exists for this (entity_type, entity_id),
        it will be updated instead of creating a new one.
        """
        # Check if customization already exists
        existing = self._repository.get_by_entity(
            entity_type=command.entity_type,
            entity_id=command.entity_id
        )
        
        if existing:
            # Update existing customization
            existing.update(
                fields=command.fields if command.fields else existing.fields,
                validation=command.validation if command.validation is not None else existing.validation,
                metadata=command.metadata if command.metadata is not None else existing.metadata
            )
            self._repository.save(existing)
        else:
            # Create new customization
            entity_customization = EntityCustomization.create(
                entity_type=command.entity_type,
                entity_id=command.entity_id,
                fields=command.fields,
                id=command.id,
                validation=command.validation,
                metadata=command.metadata
            )
            self._repository.save(entity_customization)

