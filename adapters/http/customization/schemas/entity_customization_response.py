from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional, Dict, Any

from adapters.http.customization.schemas.custom_field_response import CustomFieldResponse


class EntityCustomizationResponse(BaseModel):
    """Response schema for entity customization"""
    id: str = Field(..., description="Entity customization ID")
    entity_type: str = Field(..., description="Entity type")
    entity_id: str = Field(..., description="Entity ID")
    fields: List[CustomFieldResponse] = Field(..., description="List of custom fields")
    validation: Optional[str] = Field(None, description="JSON-Logic validation rules")
    metadata: Dict[str, Any] = Field(default_factory=dict, description="Additional metadata")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

