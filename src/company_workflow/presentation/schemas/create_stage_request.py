"""Create Stage Request Schema."""
from typing import Optional
from pydantic import BaseModel, Field


class CreateStageRequest(BaseModel):
    """Request schema for creating a workflow stage."""

    workflow_id: str = Field(..., description="ID of the workflow this stage belongs to")
    name: str = Field(..., min_length=1, max_length=200, description="Name of the stage")
    description: str = Field(..., description="Description of what happens in this stage")
    stage_type: str = Field(..., description="Type of stage: INITIAL, INTERMEDIATE, FINAL, or CUSTOM")
    order: int = Field(..., ge=1, description="Order position of the stage in the workflow")
    required_outcome: Optional[str] = Field(None, description="Required outcome: PASSED, FAILED, PENDING, or SKIPPED")
    estimated_duration_days: Optional[int] = Field(None, ge=0, description="Estimated duration in days")
    is_active: bool = Field(True, description="Whether the stage is active")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "01HQZX...",
                "name": "Initial Screening",
                "description": "First contact with the candidate",
                "stage_type": "INITIAL",
                "order": 1,
                "required_outcome": "PASSED",
                "estimated_duration_days": 2,
                "is_active": True
            }
        }
