from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WorkflowStageDto:
    """DTO for workflow stage"""
    id: str
    workflow_id: str
    name: str
    description: str
    stage_type: str
    order: int
    required_outcome: Optional[str]
    estimated_duration_days: Optional[int]
    is_active: bool
    created_at: datetime
    updated_at: datetime
