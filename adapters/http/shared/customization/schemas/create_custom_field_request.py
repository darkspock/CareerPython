from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class CreateCustomFieldRequest(BaseModel):
    """Request schema for creating a custom field"""
    field_key: str = Field(..., description="Unique field key (alphanumeric + underscore)")
    field_name: str = Field(..., description="Display name of the field")
    field_type: str = Field(..., description="Field type (TEXT, DROPDOWN, NUMBER, etc.)")
    field_config: Optional[Dict[str, Any]] = Field(None, description="Field-specific configuration")
    order_index: int = Field(..., description="Order index for display")

    class Config:
        json_schema_extra = {
            "example": {
                "field_key": "salary_range",
                "field_name": "Salary Range",
                "field_type": "CURRENCY",
                "field_config": {"currency": "USD", "min": 0, "max": 200000},
                "order_index": 0
            }
        }
