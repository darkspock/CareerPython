from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WorkflowDto:
    """DTO for workflow"""
    id: str
    company_id: str
    workflow_type: str  # WorkflowTypeEnum value
    display: str  # WorkflowDisplayEnum value
    phase_id: Optional[str]  # Phase 12: Phase association
    name: str
    description: str
    status: str  # WorkflowStatusEnum value
    is_default: bool
    created_at: datetime
    updated_at: datetime
