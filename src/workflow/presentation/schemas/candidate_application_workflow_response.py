from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


class WorkflowResponse(BaseModel):
    """Company workflow API response schema"""
    id: str
    company_id: str
    phase_id: Optional[str] = None  # Phase 12: Phase association
    name: str
    description: str
    status: str
    is_default: bool
    created_at: datetime
    updated_at: datetime

    # Optional enriched fields (populated when needed)
    stages: Optional[List[dict]] = None  # Will contain WorkflowStageResponse data
    candidate_count: Optional[int] = None
    active_candidate_count: Optional[int] = None
    active_position_count: Optional[int] = None

    class Config:
        from_attributes = True
