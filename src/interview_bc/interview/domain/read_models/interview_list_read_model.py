"""Read model for interview list with all related information"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class InterviewListReadModel:
    """
    Read model for interview list with all related information.
    Used for efficient queries with JOINs between interviews, candidates, positions, users, roles, etc.
    This is NOT a domain entity - it's a read-only data structure for queries.
    """
    # Interview fields
    id: str
    candidate_id: str
    required_roles: List[str]  # List of CompanyRole IDs
    interview_type: str
    status: str
    interviewers: List[str]  # List of CompanyUser IDs
    job_position_id: Optional[str] = None
    application_id: Optional[str] = None
    interview_template_id: Optional[str] = None
    workflow_stage_id: Optional[str] = None
    process_type: Optional[str] = None
    interview_mode: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    deadline_date: Optional[datetime] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    interviewer_notes: Optional[str] = None
    candidate_notes: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    free_answers: Optional[str] = None
    link_token: Optional[str] = None
    link_expires_at: Optional[datetime] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
    
    # Related information (from JOINs)
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    job_position_title: Optional[str] = None
    interview_template_name: Optional[str] = None
    workflow_stage_name: Optional[str] = None
    
    # Interviewers information (from JOINs)
    interviewer_names: List[str] = None  # List of interviewer names/emails
    
    # Required roles information (from JOINs)
    required_role_names: List[str] = None  # List of role names
    
    # Computed fields
    is_incomplete: bool = False  # True if has scheduled_at but missing required_roles or interviewers
    
    def __post_init__(self):
        """Initialize default values for lists"""
        if self.interviewer_names is None:
            self.interviewer_names = []
        if self.required_role_names is None:
            self.required_role_names = []
        if self.interviewers is None:
            self.interviewers = []
        if self.required_roles is None:
            self.required_roles = []

