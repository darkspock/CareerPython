from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class WorkflowDto:
    """DTO for company workflow"""
    id: str
    company_id: str
    phase_id: Optional[str]  # Phase 12: Phase association
    name: str
    description: str
    status: str
    is_default: bool
    created_at: datetime
    updated_at: datetime
