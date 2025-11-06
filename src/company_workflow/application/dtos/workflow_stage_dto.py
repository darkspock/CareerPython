from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, List


@dataclass
class WorkflowStageDto:
    """DTO for workflow stage"""
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
    next_phase_id: Optional[str]
    kanban_display: str
    style: dict
    created_at: datetime
    updated_at: datetime
