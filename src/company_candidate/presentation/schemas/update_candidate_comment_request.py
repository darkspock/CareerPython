from pydantic import BaseModel, Field
from typing import Optional


class UpdateCandidateCommentRequest(BaseModel):
    """Request schema for updating a candidate comment"""
    comment: Optional[str] = Field(default=None, description="Comment text")
    visibility: Optional[str] = Field(default=None, description="Comment visibility: 'private' or 'shared_with_candidate'")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "Updated comment text",
                "visibility": "shared_with_candidate"
            }
        }

