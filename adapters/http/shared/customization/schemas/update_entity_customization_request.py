from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from adapters.http.shared.customization.schemas.create_custom_field_request import CreateCustomFieldRequest


class UpdateEntityCustomizationRequest(BaseModel):
    """Request schema for updating an entity customization"""
    fields: Optional[List[CreateCustomFieldRequest]] = Field(None, description="List of custom fields")
    validation: Optional[str] = Field(None, description="JSON-Logic validation rules")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "fields": [
                    {
                        "field_key": "salary_range",
                        "field_name": "Salary Range",
                        "field_type": "CURRENCY",
                        "field_config": {"currency": "USD", "min": 0, "max": 200000},
                        "order_index": 0
                    }
                ],
                "validation": None,
                "metadata": {}
            }
        }

