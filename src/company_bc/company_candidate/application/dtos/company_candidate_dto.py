from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class CompanyCandidateDto:
    """Company candidate data transfer object"""
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
    # Resume fields
    lead_id: Optional[str]
    source: str
    resume_url: Optional[str]
    resume_uploaded_by: Optional[str]
    resume_uploaded_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime
