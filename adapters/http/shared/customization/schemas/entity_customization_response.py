from datetime import datetime
from typing import List, Optional, Dict, Any

from pydantic import BaseModel, Field

from adapters.http.shared.customization.schemas.custom_field_response import CustomFieldResponse


class EntityCustomizationResponse(BaseModel):
    """Response schema for entity customization"""
    id: Optional[str] = Field(None, description="Entity customization ID")
    entity_type: str = Field(..., description="Entity type")
    entity_id: str = Field(..., description="Entity ID")
    fields: List[CustomFieldResponse] = Field(default_factory=list, description="List of custom fields")
    validation: Optional[str] = Field(None, description="JSON-Logic validation rules")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")
    exists: bool = Field(True, description="Whether the customization exists in database")

    class Config:
        from_attributes = True

    @classmethod
    def empty(cls, entity_type: str, entity_id: str) -> "EntityCustomizationResponse":
        """Create an empty customization response for when none exists"""
        return cls(
            id=None,
            entity_type=entity_type,
            entity_id=entity_id,
            fields=[],
            validation=None,
            metadata={},
            created_at=None,
            updated_at=None,
            exists=False
        )
