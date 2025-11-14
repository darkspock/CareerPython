from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class WorkflowResponse(BaseModel):
    """Workflow API response schema"""
    id: str
    company_id: str
    workflow_type: str  # WorkflowTypeEnum value: 'PO', 'CA', 'CO'
    display: str  # WorkflowDisplayEnum value: 'kanban', 'list'
    phase_id: Optional[str] = None  # Phase 12: Phase association
    name: str
    description: str
    status: str  # WorkflowStatusEnum value: 'draft', 'active', 'archived'
    is_default: bool
    created_at: datetime
    updated_at: datetime

    # Optional enriched fields (populated when needed)
    stages: Optional[List[dict]] = None  # Will contain WorkflowStageResponse data

    class Config:
        from_attributes = True
