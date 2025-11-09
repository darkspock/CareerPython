from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict


@dataclass
class CompanyCandidateWithCandidateReadModel:
    """
    Read model for company candidate with candidate basic info.
    Used for efficient queries with JOIN between company_candidates and candidates tables.
    This is NOT a domain entity - it's a read-only data structure for queries.
    """
    # Company Candidate fields
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
    lead_id: Optional[str]
    source: str
    resume_url: Optional[str]
    resume_uploaded_by: Optional[str]
    resume_uploaded_at: Optional[datetime]
    created_at: datetime
    updated_at: datetime

    # Candidate basic info (from JOIN)
    candidate_name: str
    candidate_email: str
    candidate_phone: str

    # Job position info (from candidate_application JOIN)
    job_position_id: Optional[str] = None
    job_position_title: Optional[str] = None
    application_status: Optional[str] = None
    # Workflow and stage info (from workflow and stage JOINs)
    workflow_name: Optional[str] = None
    stage_name: Optional[str] = None
    # Phase info (from phase JOIN)
    phase_name: Optional[str] = None
    # Comment counts
    pending_comments_count: int = 0
