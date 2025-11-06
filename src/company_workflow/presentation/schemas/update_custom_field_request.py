from typing import Optional, Dict, Any

from pydantic import BaseModel, Field


class UpdateCustomFieldRequest(BaseModel):
    """Request schema for updating a custom field"""
    field_name: str = Field(..., description="Display name")
    field_type: str = Field(..., description="Field type")
    field_config: Optional[Dict[str, Any]] = Field(default=None, description="Field-specific configuration")

    class Config:
        json_schema_extra = {
            "example": {
                "field_name": "Expected Annual Salary",
                "field_type": "CURRENCY",
                "field_config": {
                    "currency_code": "USD",
                    "min": 30000,
                    "max": 300000
                }
            }
        }
