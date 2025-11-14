from typing import Optional

from pydantic import BaseModel, Field


class CreateReviewRequest(BaseModel):
    """Request schema for creating a candidate review"""
    score: int = Field(..., description="Review score: 0 (ban), 3 (thumbs down), 6 (thumbs up), 10 (favorite)", ge=0,
                       le=10)
    comment: Optional[str] = Field(default=None, description="Optional comment text")
    workflow_id: Optional[str] = Field(default=None, description="Workflow ID where review was made")
    stage_id: Optional[str] = Field(default=None, description="Stage ID where review was made (None = global review)")
    review_status: str = Field(default="reviewed", description="Review status: 'reviewed' or 'pending'")

    class Config:
        json_schema_extra = {
            "example": {
                "score": 6,
                "comment": "Good candidate, recommended for next stage",
                "workflow_id": "01HXXXXXXXXXXXXXXXXXXX",
                "stage_id": "01HXXXXXXXXXXXXXXXXXXX",
                "review_status": "reviewed"
            }
        }
