from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class WorkflowStageResponse(BaseModel):
    """Workflow stage API response schema"""
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

    class Config:
        from_attributes = True
