from abc import ABC, abstractmethod
from typing import Optional, List

from src.shared_bc.customization.entity_customization.domain.entities.entity_customization import EntityCustomization
from src.shared_bc.customization.entity_customization.domain.enums.entity_customization_type_enum import \
    EntityCustomizationTypeEnum
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import \
    EntityCustomizationId


class EntityCustomizationRepositoryInterface(ABC):
    """Repository interface for entity customization operations"""

    @abstractmethod
    def save(self, entity_customization: EntityCustomization) -> None:
        """Save or update an entity customization"""
        pass

    @abstractmethod
    def get_by_id(self, id: EntityCustomizationId) -> Optional[EntityCustomization]:
        """Get an entity customization by ID"""
        pass

    @abstractmethod
    def get_by_entity(
            self,
            entity_type: EntityCustomizationTypeEnum,
            entity_id: str
    ) -> Optional[EntityCustomization]:
        """Get an entity customization by entity type and entity ID"""
        pass

    @abstractmethod
    def list_by_entity_type(
            self,
            entity_type: EntityCustomizationTypeEnum
    ) -> List[EntityCustomization]:
        """List all customizations for a given entity type"""
        pass

    @abstractmethod
    def delete(self, id: EntityCustomizationId) -> None:
        """Delete an entity customization"""
        pass
