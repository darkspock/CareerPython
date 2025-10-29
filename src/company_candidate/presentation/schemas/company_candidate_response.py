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
    current_phase_id: Optional[str]  # Current recruitment phase
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
    # Candidate basic info (optional, populated when needed)
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    candidate_phone: Optional[str] = None
    # Job position info (optional, populated from candidate_application)
    job_position_id: Optional[str] = None
    job_position_title: Optional[str] = None
    application_status: Optional[str] = None

    class Config:
        from_attributes = True
