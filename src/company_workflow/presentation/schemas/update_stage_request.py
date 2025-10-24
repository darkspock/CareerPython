"""Update Stage Request Schema."""
from typing import Optional
from pydantic import BaseModel, Field


class UpdateStageRequest(BaseModel):
    """Request schema for updating a workflow stage."""

    name: str = Field(..., min_length=1, max_length=200, description="Name of the stage")
    description: str = Field(..., description="Description of what happens in this stage")
    stage_type: str = Field(..., description="Stage type: INITIAL, INTERMEDIATE, or FINAL")
    required_outcome: Optional[str] = Field(None, description="Required outcome: PASSED, FAILED, PENDING, or SKIPPED")
    estimated_duration_days: Optional[int] = Field(None, ge=0, description="Estimated duration in days")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Technical Interview",
                "description": "In-depth technical assessment",
                "stage_type": "INTERMEDIATE",
                "required_outcome": "PASSED",
                "estimated_duration_days": 3
            }
        }
