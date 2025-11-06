from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
import re

from src.customization.domain.value_objects.custom_field_id import CustomFieldId


@dataclass(frozen=True)
class CustomField:
    """Value object representing a custom field definition"""
    id: CustomFieldId
    field_key: str
    field_name: str
    field_type: str
    field_config: Optional[Dict[str, Any]]
    order_index: int
    created_at: datetime
    updated_at: datetime

    # Valid field types
    VALID_FIELD_TYPES = {
        'TEXT', 'TEXTAREA', 'NUMBER', 'CURRENCY', 'DATE',
        'DROPDOWN', 'MULTI_SELECT', 'RADIO', 'CHECKBOX',
        'FILE', 'URL', 'EMAIL', 'PHONE'
    }

    @classmethod
    def create(
        cls,
        field_key: str,
        field_name: str,
        field_type: str,
        order_index: int,
        id: Optional[CustomFieldId] = None,
        field_config: Optional[Dict[str, Any]] = None
    ) -> "CustomField":
        """Factory method to create a new custom field"""
        # Validate field_key
        if not field_key:
            raise ValueError("Field key cannot be empty")
        
        # Field key must be alphanumeric with underscores, no spaces
        if not re.match(r'^[a-zA-Z0-9_]+$', field_key):
            raise ValueError("Field key must contain only alphanumeric characters and underscores")
        
        # Validate field_name
        if not field_name:
            raise ValueError("Field name cannot be empty")
        
        # Validate field_type
        if field_type not in cls.VALID_FIELD_TYPES:
            raise ValueError(
                f"Invalid field type '{field_type}'. "
                f"Valid types are: {', '.join(sorted(cls.VALID_FIELD_TYPES))}"
            )
        
        # Validate order_index
        if order_index < 0:
            raise ValueError("Order index must be non-negative")
        
        now = datetime.utcnow()
        field_id = id or CustomFieldId.generate()
        
        return cls(
            id=field_id,
            field_key=field_key,
            field_name=field_name,
            field_type=field_type,
            field_config=field_config,
            order_index=order_index,
            created_at=now,
            updated_at=now
        )
