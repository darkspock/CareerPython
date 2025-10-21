from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict


class CompanyCandidateResponse(BaseModel):
    """Company candidate API response schema"""
    id: str
    company_id: str
    candidate_id: str
    status: str
    ownership_status: str
    created_by_user_id: str
    workflow_id: Optional[str]
    current_stage_id: Optional[str]
    invited_at: datetime
    confirmed_at: Optional[datetime]
    rejected_at: Optional[datetime]
    archived_at: Optional[datetime]
    visibility_settings: Dict[str, bool]
    tags: List[str]
    internal_notes: str
    position: Optional[str]
    department: Optional[str]
    priority: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
