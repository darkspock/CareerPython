"""Interview List DTO for application layer - uses ReadModel"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.interview_bc.interview.domain.read_models.interview_list_read_model import InterviewListReadModel


@dataclass
class InterviewListDto:
    """DTO for interview list with all related information"""
    id: str
    candidate_id: str
    candidate_name: Optional[str] = None
    candidate_email: Optional[str] = None
    required_roles: List[str] = None
    required_role_names: List[str] = None
    interview_type: str = ""
    status: str = ""
    interviewers: List[str] = None
    interviewer_names: List[str] = None
    job_position_id: Optional[str] = None
    job_position_title: Optional[str] = None
    application_id: Optional[str] = None
    interview_template_id: Optional[str] = None
    interview_template_name: Optional[str] = None
    workflow_stage_id: Optional[str] = None
    workflow_stage_name: Optional[str] = None
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
    is_incomplete: bool = False

    def __post_init__(self)->None:
        """Initialize default values for lists"""
        if self.interviewer_names is None:
            self.interviewer_names = []
        if self.required_role_names is None:
            self.required_role_names = []
        if self.interviewers is None:
            self.interviewers = []
        if self.required_roles is None:
            self.required_roles = []

    @classmethod
    def from_read_model(cls, read_model: InterviewListReadModel) -> "InterviewListDto":
        """Convert ReadModel to DTO"""
        return cls(
            id=read_model.id,
            candidate_id=read_model.candidate_id,
            candidate_name=read_model.candidate_name,
            candidate_email=read_model.candidate_email,
            required_roles=read_model.required_roles,
            required_role_names=read_model.required_role_names,
            interview_type=read_model.interview_type,
            status=read_model.status,
            interviewers=read_model.interviewers,
            interviewer_names=read_model.interviewer_names,
            job_position_id=read_model.job_position_id,
            job_position_title=read_model.job_position_title,
            application_id=read_model.application_id,
            interview_template_id=read_model.interview_template_id,
            interview_template_name=read_model.interview_template_name,
            workflow_stage_id=read_model.workflow_stage_id,
            workflow_stage_name=read_model.workflow_stage_name,
            process_type=read_model.process_type,
            interview_mode=read_model.interview_mode,
            title=read_model.title,
            description=read_model.description,
            scheduled_at=read_model.scheduled_at,
            deadline_date=read_model.deadline_date,
            started_at=read_model.started_at,
            finished_at=read_model.finished_at,
            duration_minutes=read_model.duration_minutes,
            interviewer_notes=read_model.interviewer_notes,
            candidate_notes=read_model.candidate_notes,
            score=read_model.score,
            feedback=read_model.feedback,
            free_answers=read_model.free_answers,
            link_token=read_model.link_token,
            link_expires_at=read_model.link_expires_at,
            created_at=read_model.created_at,
            updated_at=read_model.updated_at,
            created_by=read_model.created_by,
            updated_by=read_model.updated_by,
            is_incomplete=read_model.is_incomplete
        )

