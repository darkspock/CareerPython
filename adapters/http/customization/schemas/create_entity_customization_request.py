from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

from adapters.http.customization.schemas.create_custom_field_request import CreateCustomFieldRequest


class CreateEntityCustomizationRequest(BaseModel):
    """Request schema for creating an entity customization"""
    entity_type: str = Field(..., description="Entity type (JobPosition, CandidateApplication, Candidate)")
    entity_id: str = Field(..., description="Entity ID")
    fields: List[CreateCustomFieldRequest] = Field(default_factory=list, description="List of custom fields")
    validation: Optional[str] = Field(None, description="JSON-Logic validation rules")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Additional metadata")

    class Config:
        json_schema_extra: Dict[str, Any] = {
            "example": {
                "entity_type": "JobPosition",
                "entity_id": "01HXXXXXXXXXXXXXXXXXXX",
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

