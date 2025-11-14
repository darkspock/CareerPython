"""Job Position Comment Schemas."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CreateJobPositionCommentRequest(BaseModel):
    """Request schema for creating a job position comment"""
    comment: str = Field(..., min_length=1, description="Comment text content")
    workflow_id: Optional[str] = Field(None, description="Workflow ID (optional)")
    stage_id: Optional[str] = Field(None, description="Stage ID (null = global comment)")
    visibility: str = Field("shared", description="Comment visibility: private or shared")
    review_status: str = Field("reviewed", description="Review status: pending or reviewed")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "This position needs review before publishing",
                "stage_id": None,
                "visibility": "private",
                "review_status": "reviewed"
            }
        }


class UpdateJobPositionCommentRequest(BaseModel):
    """Request schema for updating a job position comment"""
    comment: Optional[str] = Field(None, min_length=1, description="Updated comment text")
    visibility: Optional[str] = Field(None, description="Updated visibility: private or shared")

    class Config:
        json_schema_extra = {
            "example": {
                "comment": "Updated comment text",
                "visibility": "shared"
            }
        }


class JobPositionCommentResponse(BaseModel):
    """Response schema for a job position comment"""
    id: str
    job_position_id: str
    comment: str
    workflow_id: Optional[str]
    stage_id: Optional[str]  # null = global comment
    created_by_user_id: str
    review_status: str
    visibility: str
    created_at: datetime
    updated_at: datetime
    is_global: bool

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01H...",
                "job_position_id": "01H...",
                "comment": "Great candidate for this role",
                "workflow_id": "01H...",
                "stage_id": None,
                "created_by_user_id": "01H...",
                "review_status": "reviewed",
                "visibility": "private",
                "created_at": "2025-01-15T10:30:00",
                "updated_at": "2025-01-15T10:30:00",
                "is_global": True
            }
        }


class JobPositionCommentListResponse(BaseModel):
    """Response schema for list of job position comments"""
    comments: list[JobPositionCommentResponse]
    total: int

    class Config:
        json_schema_extra = {
            "example": {
                "comments": [],
                "total": 0
            }
        }
