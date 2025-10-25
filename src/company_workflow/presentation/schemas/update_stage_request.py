"""Update Stage Request Schema."""
from typing import Optional, List
from decimal import Decimal
from pydantic import BaseModel, Field


class UpdateStageRequest(BaseModel):
    """Request schema for updating a workflow stage."""

    name: str = Field(..., min_length=1, max_length=200, description="Name of the stage")
    description: str = Field(..., description="Description of what happens in this stage")
    stage_type: str = Field(..., description="Stage type: INITIAL, INTERMEDIATE, or FINAL")
    allow_skip: bool = Field(False, description="Whether this stage can be skipped (optional stage)")
    estimated_duration_days: Optional[int] = Field(None, ge=0, description="Estimated duration in days")
    default_role_ids: Optional[List[str]] = Field(None, description="Default roles assigned to this stage")
    default_assigned_users: Optional[List[str]] = Field(None, description="Default user IDs always assigned to this stage")
    email_template_id: Optional[str] = Field(None, description="Email template ID to use when entering this stage")
    custom_email_text: Optional[str] = Field(None, description="Custom email text to append to template")
    deadline_days: Optional[int] = Field(None, ge=1, description="Days to complete this stage (for task priority)")
    estimated_cost: Optional[Decimal] = Field(None, ge=0, description="Estimated cost for this stage")

    class Config:
        json_schema_extra = {
            "example": {
                "name": "Technical Interview",
                "description": "In-depth technical assessment",
                "stage_type": "INTERMEDIATE",
                "allow_skip": False,
                "estimated_duration_days": 3,
                "default_role_ids": ["tech_lead", "senior_developer"],
                "default_assigned_users": ["user_id_2"],
                "email_template_id": "template_456",
                "custom_email_text": "Please prepare for technical questions",
                "deadline_days": 5,
                "estimated_cost": "100.00"
            }
        }
