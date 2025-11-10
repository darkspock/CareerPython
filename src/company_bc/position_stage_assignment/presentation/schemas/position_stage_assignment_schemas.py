"""Position stage assignment request and response schemas"""
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel, Field


class AssignUsersToStageRequest(BaseModel):
    """Request schema for assigning users to a stage"""
    position_id: str = Field(..., description="Position ID")
    stage_id: str = Field(..., description="Stage ID")
    user_ids: List[str] = Field(..., description="List of user IDs to assign")

    class Config:
        json_schema_extra = {
            "example": {
                "position_id": "01HQWXYZ123456789ABCDEFGHI",
                "stage_id": "01HQWXYZ123456789ABCDEFGHJ",
                "user_ids": ["user1", "user2", "user3"]
            }
        }


class AddUserToStageRequest(BaseModel):
    """Request schema for adding a user to a stage"""
    position_id: str = Field(..., description="Position ID")
    stage_id: str = Field(..., description="Stage ID")
    user_id: str = Field(..., description="User ID to add")

    class Config:
        json_schema_extra = {
            "example": {
                "position_id": "01HQWXYZ123456789ABCDEFGHI",
                "stage_id": "01HQWXYZ123456789ABCDEFGHJ",
                "user_id": "user1"
            }
        }


class RemoveUserFromStageRequest(BaseModel):
    """Request schema for removing a user from a stage"""
    position_id: str = Field(..., description="Position ID")
    stage_id: str = Field(..., description="Stage ID")
    user_id: str = Field(..., description="User ID to remove")

    class Config:
        json_schema_extra = {
            "example": {
                "position_id": "01HQWXYZ123456789ABCDEFGHI",
                "stage_id": "01HQWXYZ123456789ABCDEFGHJ",
                "user_id": "user1"
            }
        }


class WorkflowStageAssignmentRequest(BaseModel):
    """Request schema for workflow stage assignment"""
    stage_id: str = Field(..., description="Stage ID")
    default_user_ids: List[str] = Field(..., description="Default user IDs for this stage")

    class Config:
        json_schema_extra = {
            "example": {
                "stage_id": "01HQWXYZ123456789ABCDEFGHJ",
                "default_user_ids": ["user1", "user2"]
            }
        }


class CopyWorkflowAssignmentsRequest(BaseModel):
    """Request schema for copying workflow assignments"""
    position_id: str = Field(..., description="Position ID")
    workflow_assignments: List[WorkflowStageAssignmentRequest] = Field(
        ...,
        description="List of workflow stage assignments to copy"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "position_id": "01HQWXYZ123456789ABCDEFGHI",
                "workflow_assignments": [
                    {
                        "stage_id": "01HQWXYZ123456789ABCDEFGHJ",
                        "default_user_ids": ["user1", "user2"]
                    },
                    {
                        "stage_id": "01HQWXYZ123456789ABCDEFGHK",
                        "default_user_ids": ["user3"]
                    }
                ]
            }
        }


class PositionStageAssignmentResponse(BaseModel):
    """Response schema for position stage assignment"""
    id: str = Field(..., description="Assignment ID")
    position_id: str = Field(..., description="Position ID")
    stage_id: str = Field(..., description="Stage ID")
    assigned_user_ids: List[str] = Field(..., description="List of assigned user IDs")
    created_at: Optional[datetime] = Field(None, description="Creation timestamp")
    updated_at: Optional[datetime] = Field(None, description="Last update timestamp")

    class Config:
        json_schema_extra = {
            "example": {
                "id": "01HQWXYZ123456789ABCDEFGHL",
                "position_id": "01HQWXYZ123456789ABCDEFGHI",
                "stage_id": "01HQWXYZ123456789ABCDEFGHJ",
                "assigned_user_ids": ["user1", "user2", "user3"],
                "created_at": "2024-01-15T10:00:00",
                "updated_at": "2024-01-15T10:00:00"
            }
        }
