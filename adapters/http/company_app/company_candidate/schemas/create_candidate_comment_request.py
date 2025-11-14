from typing import Optional

from pydantic import BaseModel, Field


class CreateCandidateCommentRequest(BaseModel):
    """Request schema for creating a candidate comment"""
    comment: str = Field(..., description="Comment text")
    workflow_id: Optional[str] = Field(default=None, description="Workflow ID where comment was made")
    stage_id: Optional[str] = Field(default=None, description="Stage ID where comment was made")
    visibility: str = Field(default="private", description="Comment visibility: 'private' or 'shared_with_candidate'")
    review_status: str = Field(default="reviewed", description="Review status: 'reviewed' or 'pending'")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "Strong candidate with excellent Python skills",
                "workflow_id": "01HXXXXXXXXXXXXXXXXXXX",
                "stage_id": "01HXXXXXXXXXXXXXXXXXXX",
                "visibility": "private",
                "review_status": "reviewed"
            }
        }
