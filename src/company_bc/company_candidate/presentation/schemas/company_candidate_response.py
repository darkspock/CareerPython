from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List, Dict, Any


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
    phase_id: Optional[str]  # Current recruitment phase
    invited_at: datetime
    confirmed_at: Optional[datetime]
    rejected_at: Optional[datetime]
    archived_at: Optional[datetime]
    visibility_settings: Dict[str, bool]
    tags: List[str]
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
    # Workflow and stage info (optional, populated when needed)
    stage_name: Optional[str] = None
    workflow_name: Optional[str] = None
    # Phase info (optional, populated when needed)
    phase_name: Optional[str] = None
    # Custom field values (optional, populated when needed)
    custom_field_values: Optional[Dict[str, Any]] = None
    # Comment counts (optional, populated when needed)
    pending_comments_count: int = 0

    class Config:
        from_attributes = True
