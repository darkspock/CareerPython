from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any


class CustomFieldResponse(BaseModel):
    """Response schema for custom field"""
    id: str = Field(..., description="Custom field ID")
    entity_customization_id: str = Field(..., description="Entity customization ID")
    field_key: str = Field(..., description="Unique field key")
    field_name: str = Field(..., description="Display name")
    field_type: str = Field(..., description="Field type")
    field_config: Optional[Dict[str, Any]] = Field(None, description="Field configuration")
    order_index: int = Field(..., description="Order index")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True

