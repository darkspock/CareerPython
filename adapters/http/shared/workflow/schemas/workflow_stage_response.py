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
    next_phase_id: Optional[str] = None  # Phase 12: Phase transition
    kanban_display: str  # Kanban display configuration: 'column', 'row', 'hidden'
    style: dict  # Visual styling: {background_color, text_color, icon}
    validation_rules: Optional[dict] = None  # JsonLogic validation rules
    recommended_rules: Optional[dict] = None  # JsonLogic recommendation rules
    interview_configurations: Optional[List[dict]] = None  # List of interview configurations: [{"template_id": str, "mode": str}]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
