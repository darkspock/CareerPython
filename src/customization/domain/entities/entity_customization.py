from dataclasses import dataclass, field
from datetime import datetime
from typing import List, Dict, Any, Optional

from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from src.customization.domain.value_objects.custom_field import CustomField
from src.customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.customization.domain.value_objects.custom_field_id import CustomFieldId


@dataclass
class EntityCustomization:
    """Entity customization - allows customizing any entity with custom fields"""
    id: EntityCustomizationId
    entity_type: EntityCustomizationTypeEnum
    entity_id: str
    fields: List[CustomField]
    validation: Optional[str]  # JSON-Logic validation rules
    created_at: datetime
    updated_at: datetime
    metadata: Dict[str, Any] = field(default_factory=dict)

    @classmethod
    def create(
        cls,
        entity_type: EntityCustomizationTypeEnum,
        entity_id: str,
        fields: List[CustomField],
        id: Optional[EntityCustomizationId] = None,
        validation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> "EntityCustomization":
        """Factory method to create a new entity customization"""
        if not entity_id:
            raise ValueError("Entity ID cannot be empty")
        
        if not isinstance(entity_type, EntityCustomizationTypeEnum):
            raise ValueError("Invalid entity type")
        
        # Validate JSON-Logic if provided
        if validation:
            # TODO: Add JSON-Logic validation
            pass
        
        now = datetime.utcnow()
        customization_id = id or EntityCustomizationId.generate()
        
        return cls(
            id=customization_id,
            entity_type=entity_type,
            entity_id=entity_id,
            fields=fields or [],
            validation=validation,
            created_at=now,
            updated_at=now,
            metadata=metadata or {}
        )

    def update(
        self,
        fields: Optional[List[CustomField]] = None,
        validation: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """Update entity customization"""
        if fields is not None:
            self.fields = fields
        
        if validation is not None:
            # TODO: Validate JSON-Logic
            self.validation = validation
        
        if metadata is not None:
            self.metadata = metadata
        
        self.updated_at = datetime.utcnow()

    def add_field(self, field: CustomField) -> None:
        """Add a custom field to this customization"""
        # Check if field_key already exists
        if any(f.field_key == field.field_key for f in self.fields):
            raise ValueError(f"Field with key '{field.field_key}' already exists")
        
        self.fields.append(field)
        self.updated_at = datetime.utcnow()

    def remove_field(self, field_id: CustomFieldId) -> None:
        """Remove a custom field from this customization"""
        from src.customization.domain.exceptions.custom_field_not_found import CustomFieldNotFound
        
        field_to_remove = next((f for f in self.fields if str(f.id) == str(field_id)), None)
        if not field_to_remove:
            raise CustomFieldNotFound(f"Field with ID '{field_id}' not found")
        
        self.fields.remove(field_to_remove)
        self.updated_at = datetime.utcnow()

    def update_field(self, field_id: CustomFieldId, field: CustomField) -> None:
        """Update a custom field in this customization"""
        from src.customization.domain.exceptions.custom_field_not_found import CustomFieldNotFound
        
        field_index = next((i for i, f in enumerate(self.fields) if str(f.id) == str(field_id)), None)
        if field_index is None:
            raise CustomFieldNotFound(f"Field with ID '{field_id}' not found")
        
        # If field_key is changing, check it doesn't conflict
        if field.field_key != self.fields[field_index].field_key:
            if any(f.field_key == field.field_key for f in self.fields):
                raise ValueError(f"Field with key '{field.field_key}' already exists")
        
        self.fields[field_index] = field
        self.updated_at = datetime.utcnow()

    def reorder_fields(self, field_ids_in_order: List[CustomFieldId]) -> None:
        """Reorder fields according to the provided list of field IDs"""
        from src.customization.domain.exceptions.custom_field_not_found import CustomFieldNotFound
        
        if len(field_ids_in_order) != len(self.fields):
            raise ValueError("Number of field IDs must match number of fields")
        
        # Create a map of field_id (as string) -> field
        field_map = {str(f.id): f for f in self.fields}
        
        # Verify all field IDs exist
        for field_id in field_ids_in_order:
            if str(field_id) not in field_map:
                raise CustomFieldNotFound(f"Field with ID '{field_id}' not found")
        
        # Reorder fields
        self.fields = [field_map[str(field_id)] for field_id in field_ids_in_order]
        self.updated_at = datetime.utcnow()

