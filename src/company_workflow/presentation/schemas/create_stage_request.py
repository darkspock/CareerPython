"""Create Stage Request Schema."""
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field


class CreateStageRequest(BaseModel):
    """Request schema for creating a workflow stage."""

    workflow_id: str = Field(..., description="ID of the workflow this stage belongs to")
    name: str = Field(..., min_length=1, max_length=200, description="Name of the stage")
    description: str = Field(..., description="Description of what happens in this stage")
    stage_type: str = Field(..., description="Type of stage: INITIAL, INTERMEDIATE, FINAL, or CUSTOM")
    order: int = Field(..., ge=1, description="Order position of the stage in the workflow")
    allow_skip: bool = Field(False, description="Whether this stage can be skipped (optional stage)")
    estimated_duration_days: Optional[int] = Field(None, ge=0, description="Estimated duration in days")
    is_active: bool = Field(True, description="Whether the stage is active")
    default_role_ids: Optional[List[str]] = Field(None, description="Default roles assigned to this stage")
    default_assigned_users: Optional[List[str]] = Field(None, description="Default user IDs always assigned to this stage")
    email_template_id: Optional[str] = Field(None, description="Email template ID to use when entering this stage")
    custom_email_text: Optional[str] = Field(None, description="Custom email text to append to template")
    deadline_days: Optional[int] = Field(None, ge=1, description="Days to complete this stage (for task priority)")
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="Estimated cost for this stage")
    next_phase_id: Optional[str] = Field(None, description="Phase ID to transition to (Phase 12 - only for SUCCESS/FAIL stages)")

    class Config:
        json_schema_extra = {
            "example": {
                "workflow_id": "01HQZX...",
                "name": "Initial Screening",
                "description": "First contact with the candidate",
                "stage_type": "INITIAL",
                "order": 1,
                "allow_skip": False,
                "estimated_duration_days": 2,
                "is_active": True,
                "default_role_ids": ["recruiter", "hiring_manager"],
                "default_assigned_users": ["user_id_1"],
                "email_template_id": "template_123",
                "custom_email_text": "Looking forward to speaking with you",
                "deadline_days": 3,
                "estimated_cost": "50.00"
            }
        }
