from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any
from decimal import Decimal


@dataclass
class WorkflowStageDto:
    """DTO for workflow stage"""
    id: str
    workflow_id: str
    name: str
    description: str
    stage_type: str  # WorkflowStageTypeEnum value
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
    next_phase_id: Optional[str]  # Phase 12: Phase transition
    kanban_display: str  # KanbanDisplayEnum value
    style: Dict[str, Any]  # WorkflowStageStyle as dict
    validation_rules: Optional[Dict[str, Any]]  # JsonLogic validation rules
    recommended_rules: Optional[Dict[str, Any]]  # JsonLogic recommendation rules
    interview_configurations: Optional[List[Dict[str, str]]]  # List of interview configurations: [{"template_id": str, "mode": str}]
    created_at: datetime
    updated_at: datetime
