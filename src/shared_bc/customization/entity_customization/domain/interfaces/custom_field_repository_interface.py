from abc import ABC, abstractmethod
from typing import Optional, List

from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field import CustomField
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field_id import CustomFieldId
from src.shared_bc.customization.entity_customization.domain.value_objects.entity_customization_id import EntityCustomizationId


class CustomFieldRepositoryInterface(ABC):
    """Repository interface for custom field operations"""

    @abstractmethod
    def save(self, custom_field: CustomField, entity_customization_id: EntityCustomizationId) -> None:
        """Save or update a custom field"""
        pass

    @abstractmethod
    def get_by_id(self, custom_field_id: CustomFieldId) -> Optional[CustomField]:
        """Get a custom field by ID"""
        pass

    @abstractmethod
    def list_by_entity_customization(
        self,
        entity_customization_id: EntityCustomizationId
    ) -> List[CustomField]:
        """List all custom fields for an entity customization, ordered by order_index"""
        pass

    @abstractmethod
    def get_by_entity_customization_and_key(
        self,
        entity_customization_id: EntityCustomizationId,
        field_key: str
    ) -> Optional[CustomField]:
        """Get a custom field by entity customization ID and field key"""
        pass

    @abstractmethod
    def delete(self, custom_field_id: CustomFieldId) -> None:
        """Delete a custom field"""
        pass

