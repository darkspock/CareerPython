"""Job Position Activity Schemas."""
from datetime import datetime
from typing import Dict, Any
from pydantic import BaseModel


class JobPositionActivityResponse(BaseModel):
    """Response schema for a job position activity"""
    id: str
    job_position_id: str
    activity_type: str
    description: str
    performed_by_user_id: str
    metadata: Dict[str, Any]
    created_at: datetime

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "01H...",
                "job_position_id": "01H...",
                "activity_type": "stage_moved",
                "description": "Moved from 'Draft' to 'Active'",
                "performed_by_user_id": "01H...",
                "metadata": {
                    "old_stage_id": "01H...",
                    "old_stage_name": "Draft",
                    "new_stage_id": "01H...",
                    "new_stage_name": "Active"
                },
                "created_at": "2025-01-15T10:30:00"
            }
        }


class JobPositionActivityListResponse(BaseModel):
    """Response schema for list of job position activities"""
    activities: list[JobPositionActivityResponse]
    total: int
    
    class Config:
        json_schema_extra = {
            "example": {
                "activities": [],
                "total": 0
            }
        }

