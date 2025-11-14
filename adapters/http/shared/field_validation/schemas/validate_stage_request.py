from typing import Dict, Any, Optional

from pydantic import BaseModel, Field


class ValidateStageRequest(BaseModel):
    """Request schema for validating a stage transition."""

    stage_id: str = Field(..., description="Workflow stage ID")
    candidate_field_values: Dict[str, Any] = Field(...,
                                                   description="Candidate's field values (custom_field_id -> value)")
    position_data: Optional[Dict[str, Any]] = Field(None, description="Position data for comparison rules")

    class Config:
        json_schema_extra = {
            "example": {
                "stage_id": "01H2X3Y4Z5A6B7C8D9E0F1G2H4",
                "candidate_field_values": {
                    "01H2X3Y4Z5A6B7C8D9E0F1G2H3": 85000
                },
                "position_data": {
                    "salary": {
                        "min": 50000,
                        "max": 80000
                    }
                }
            }
        }
