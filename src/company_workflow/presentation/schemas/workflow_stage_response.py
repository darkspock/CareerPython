from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from decimal import Decimal


class WorkflowStageResponse(BaseModel):
    """Workflow stage API response schema"""
    id: str
    workflow_id: str
    name: str
    description: str
    stage_type: str
    order: int
    allow_skip: bool
    estimated_duration_days: Optional[int]
    is_active: bool
    default_role_ids: Optional[List[str]]
    default_assigned_users: Optional[List[str]]
    email_template_id: Optional[str]
    custom_email_text: Optional[str]
    deadline_days: Optional[int]
    estimated_cost: Optional[Decimal]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
