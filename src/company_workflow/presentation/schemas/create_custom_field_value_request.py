from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class CreateCustomFieldValueRequest(BaseModel):
    """Request schema for creating a custom field value"""
    company_candidate_id: str = Field(..., description="Company candidate ID")
    workflow_id: str = Field(..., description="Workflow ID")
    values: Optional[Dict[str, Any]] = Field(default=None, description="Dictionary of field_key -> value")

    class Config:
        json_schema_extra = {
            "example": {
                "company_candidate_id": "01HXXXXXXXXXXXXXXXXXXX",
                "workflow_id": "01HXXXXXXXXXXXXXXXXXXX",
                "values": {
                    "salary": "50000",
                    "availability": "Immediate"
                }
            }
        }
