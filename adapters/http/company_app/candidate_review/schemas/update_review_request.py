from typing import Optional

from pydantic import BaseModel, Field


class UpdateReviewRequest(BaseModel):
    """Request schema for updating a candidate review"""
    score: Optional[int] = Field(default=None, description="Review score: 0, 3, 6, 10", ge=0, le=10)
    comment: Optional[str] = Field(default=None, description="Comment text (can be empty to clear)")

    class Config:
        json_schema_extra = {
            "example": {
                "score": 10,
                "comment": "Updated: Excellent candidate!"
            }
        }
