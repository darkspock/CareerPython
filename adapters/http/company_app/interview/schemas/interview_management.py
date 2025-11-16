"""
Interview management schemas for admin interview operations
"""
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from core.config import settings
from src.candidate_bc.candidate.application import GetCandidateByIdQuery
from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.company_bc.job_position.application import GetJobPositionByIdQuery
from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.framework.application import QueryBus
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.application.queries.dtos.interview_list_dto import InterviewListDto
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewTypeEnum
)


class InterviewCreateRequest(BaseModel):
    """Request schema for creating an interview"""
    candidate_id: str = Field(..., description="ID of the candidate")
    required_roles: List[str] = Field(..., min_length=1, description="List of CompanyRole IDs (obligatory)")
    interview_type: str = Field(default=InterviewTypeEnum.CUSTOM.value, description="Type of interview")
    interview_mode: str = Field(..., description="Interview mode (AUTOMATIC, AI, MANUAL)")
    process_type: Optional[str] = Field(None,
                                        description="Process type (CANDIDATE_SIGN_UP, CANDIDATE_APPLICATION, SCREENING, INTERVIEW, FEEDBACK)")
    job_position_id: Optional[str] = Field(None, description="ID of the job position")
    application_id: Optional[str] = Field(None, description="ID of the candidate application")
    interview_template_id: Optional[str] = Field(None, description="ID of the interview template")
    workflow_stage_id: Optional[str] = Field(None,
                                             description="ID of the workflow stage where this interview is conducted")
    title: Optional[str] = Field(None, description="Interview title")
    description: Optional[str] = Field(None, description="Interview description")
    scheduled_at: Optional[str] = Field(None, description="Scheduled datetime (ISO format)")
    deadline_date: Optional[str] = Field(None, description="Deadline datetime (ISO format)")
    interviewers: Optional[List[str]] = Field(None, description="List of interviewer names")


class InterviewUpdateRequest(BaseModel):
    """Request schema for updating an interview"""
    title: Optional[str] = Field(None, description="Interview title")
    description: Optional[str] = Field(None, description="Interview description")
    process_type: Optional[str] = Field(None,
                                        description="Process type (CANDIDATE_SIGN_UP, CANDIDATE_APPLICATION, SCREENING, INTERVIEW, FEEDBACK)")
    interview_type: Optional[str] = Field(None, description="Interview type")
    interview_mode: Optional[str] = Field(None, description="Interview mode (AUTOMATIC, AI, MANUAL)")
    scheduled_at: Optional[str] = Field(None, description="Scheduled datetime (ISO format)")
    deadline_date: Optional[str] = Field(None, description="Deadline datetime (ISO format)")
    required_roles: Optional[List[str]] = Field(None, min_length=1, description="List of CompanyRole IDs")
    interviewers: Optional[List[str]] = Field(None, description="List of interviewer names")
    interviewer_notes: Optional[str] = Field(None, description="Interviewer notes")
    feedback: Optional[str] = Field(None, description="Interview feedback")
    score: Optional[float] = Field(None, ge=0, le=100, description="Interview score (0-100)")


class InterviewManagementResponse(BaseModel):
    """Response schema for interview management data"""
    id: str = Field(..., description="Interview ID")
    candidate_id: str = Field(..., description="Candidate ID")
    candidate_name: Optional[str] = Field(None, description="Candidate name")
    candidate_email: Optional[str] = Field(None, description="Candidate email")
    required_roles: List[str] = Field(default_factory=list, description="List of CompanyRole IDs (obligatory)")
    required_role_names: List[str] = Field(default_factory=list, description="List of CompanyRole names")
    job_position_id: Optional[str] = Field(None, description="Job position ID")
    job_position_title: Optional[str] = Field(None, description="Job position title")
    application_id: Optional[str] = Field(None, description="Application ID")
    interview_template_id: Optional[str] = Field(None, description="Interview template ID")
    interview_template_name: Optional[str] = Field(None, description="Interview template name")
    workflow_stage_id: Optional[str] = Field(None, description="Workflow stage ID where this interview is conducted")
    workflow_stage_name: Optional[str] = Field(None, description="Workflow stage name")
    process_type: Optional[str] = Field(None,
                                        description="Process type (CANDIDATE_SIGN_UP, CANDIDATE_APPLICATION, SCREENING, INTERVIEW, FEEDBACK)")
    interview_type: str = Field(..., description="Interview type")
    interview_mode: Optional[str] = Field(None, description="Interview mode (AUTOMATIC, AI, MANUAL)")
    status: str = Field(..., description="Interview status")
    title: Optional[str] = Field(None, description="Interview title")
    description: Optional[str] = Field(None, description="Interview description")
    scheduled_at: Optional[datetime] = Field(None, description="Scheduled datetime")
    deadline_date: Optional[datetime] = Field(None, description="Deadline datetime")
    started_at: Optional[datetime] = Field(None, description="Started datetime")
    finished_at: Optional[datetime] = Field(None, description="Finished datetime")
    duration_minutes: Optional[int] = Field(None, description="Duration in minutes")
    interviewers: List[str] = Field(default_factory=list, description="List of interviewer IDs")
    interviewer_names: List[str] = Field(default_factory=list, description="List of interviewer names/emails")
    interviewer_notes: Optional[str] = Field(None, description="Interviewer notes")
    candidate_notes: Optional[str] = Field(None, description="Candidate notes")
    score: Optional[float] = Field(None, description="Interview score")
    feedback: Optional[str] = Field(None, description="Interview feedback")
    free_answers: Optional[str] = Field(None, description="Free text answers")
    link_token: Optional[str] = Field(None, description="Unique token for secure interview link access")
    link_expires_at: Optional[datetime] = Field(None, description="Expiration date for the interview link")
    shareable_link: Optional[str] = Field(None, description="Shareable link for the interview (computed)")
    is_incomplete: bool = Field(default=False,
                                description="True if has scheduled_at but missing required_roles or interviewers")
    created_at: Optional[datetime] = Field(None, description="Created datetime")
    updated_at: Optional[datetime] = Field(None, description="Updated datetime")

    @classmethod
    def from_dto(cls, queryBus: QueryBus, dto: InterviewDto) -> "InterviewManagementResponse":
        """Convert DTO to response schema"""
        candidate: Optional[CandidateDto] = queryBus.query(GetCandidateByIdQuery(dto.candidate_id))
        if not candidate:
            raise ValueError(f"Candidate with id {dto.candidate_id} not found")

        job_position: JobPositionDto = queryBus.query(GetJobPositionByIdQuery(dto.job_position_id))
        if not job_position:
            raise ValueError(f"Job position with id {dto.job_position_id} not found")

        return cls(
            id=dto.id.value,
            candidate_id=dto.candidate_id.value,
            candidate_name=candidate.name,
            candidate_email=candidate.email,
            required_roles=dto.required_roles,
            job_position_id=dto.job_position_id.value if dto.job_position_id else None,
            job_position_title=job_position.title,
            application_id=dto.application_id.value if dto.application_id else None,
            interview_template_id=dto.interview_template_id.value if dto.interview_template_id else None,
            workflow_stage_id=dto.workflow_stage_id.value if dto.workflow_stage_id else None,
            process_type=dto.process_type,
            interview_type=dto.interview_type,
            interview_mode=dto.interview_mode,
            status=dto.status,
            title=dto.title,
            description=dto.description,
            scheduled_at=dto.scheduled_at,
            deadline_date=dto.deadline_date,
            started_at=dto.started_at,
            finished_at=dto.finished_at,
            duration_minutes=dto.duration_minutes,
            interviewers=dto.interviewers,
            interviewer_notes=dto.interviewer_notes,
            candidate_notes=dto.candidate_notes,
            score=dto.score,
            feedback=dto.feedback,
            free_answers=dto.free_answers,
            link_token=dto.link_token,
            link_expires_at=dto.link_expires_at,
            shareable_link=cls._generate_shareable_link(dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
                                                        dto.link_token) if dto.link_token else None,
            is_incomplete=dto.is_incomplete,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @classmethod
    def from_list_dto(cls, dto: InterviewListDto) -> "InterviewManagementResponse":
        """Convert InterviewListDto to response schema"""

        return cls(
            id=dto.id,
            candidate_id=dto.candidate_id,
            candidate_name=dto.candidate_name,
            candidate_email=dto.candidate_email,
            required_roles=dto.required_roles if dto.required_roles else [],
            required_role_names=dto.required_role_names if dto.required_role_names else [],
            job_position_id=dto.job_position_id,
            job_position_title=dto.job_position_title,
            application_id=dto.application_id,
            interview_template_id=dto.interview_template_id,
            interview_template_name=dto.interview_template_name,
            workflow_stage_id=dto.workflow_stage_id,
            workflow_stage_name=dto.workflow_stage_name,
            process_type=dto.process_type,
            interview_type=dto.interview_type,
            interview_mode=dto.interview_mode,
            status=dto.status,
            title=dto.title,
            description=dto.description,
            scheduled_at=dto.scheduled_at,
            deadline_date=dto.deadline_date,
            started_at=dto.started_at,
            finished_at=dto.finished_at,
            duration_minutes=dto.duration_minutes,
            interviewers=dto.interviewers if dto.interviewers else [],
            interviewer_names=dto.interviewer_names if dto.interviewer_names else [],
            interviewer_notes=dto.interviewer_notes,
            candidate_notes=dto.candidate_notes,
            score=dto.score,
            feedback=dto.feedback,
            free_answers=dto.free_answers,
            link_token=dto.link_token,
            link_expires_at=dto.link_expires_at,
            shareable_link=cls._generate_shareable_link(dto.id, dto.link_token) if dto.link_token else None,
            is_incomplete=dto.is_incomplete,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @staticmethod
    def _generate_shareable_link(interview_id: str, link_token: Optional[str]) -> Optional[str]:
        """Generate shareable link for interview"""
        if not link_token:
            return None
        return f"{settings.FRONTEND_URL}/interviews/{interview_id}/access?token={link_token}"

    model_config = ConfigDict(from_attributes=True)


class InterviewListResponse(BaseModel):
    """Response schema for interview list"""
    interviews: List[InterviewManagementResponse] = Field(..., description="List of interviews")
    total: int = Field(..., description="Total number of interviews")
    page: int = Field(..., description="Current page")
    page_size: int = Field(..., description="Page size")


class InterviewStatsResponse(BaseModel):
    """Response schema for interview statistics"""
    total_interviews: int = Field(default=0, description="Total number of interviews")
    scheduled_interviews: int = Field(default=0, description="Number of scheduled interviews")
    in_progress_interviews: int = Field(default=0, description="Number of in-progress interviews")
    completed_interviews: int = Field(default=0, description="Number of completed interviews")
    average_score: Optional[float] = Field(None, description="Average interview score")
    average_duration_minutes: Optional[float] = Field(None, description="Average duration in minutes")
    pending_to_plan: int = Field(default=0,
                                 description="Interviews pending to plan (no scheduled_at or no interviewers)")
    planned: int = Field(default=0, description="Planned interviews (with scheduled_at and interviewers)")
    recently_finished: int = Field(default=0, description="Recently finished interviews (last 30 days)")
    overdue: int = Field(default=0, description="Overdue interviews (deadline_date < now and not finished)")
    pending_feedback: int = Field(default=0,
                                  description="Interviews pending feedback (finished but no score or feedback)")


class InterviewActionResponse(BaseModel):
    """Response schema for interview actions"""
    message: str = Field(..., description="Action result message")
    status: str = Field(..., description="Action status")
    interview_id: Optional[str] = Field(None, description="Interview ID")


class InterviewScoreSummaryResponse(BaseModel):
    """Response schema for interview score summary"""
    interview_id: str = Field(..., description="Interview ID")
    overall_score: Optional[float] = Field(None, description="Overall interview score")
    total_questions: int = Field(..., description="Total number of questions")
    answered_questions: int = Field(..., description="Number of answered questions")
    average_answer_score: Optional[float] = Field(None, description="Average answer score")
    completion_percentage: float = Field(..., description="Interview completion percentage")

    model_config = ConfigDict(from_attributes=True)


class ScheduledInterviewsRequest(BaseModel):
    """Request schema for getting scheduled interviews"""
    from_date: Optional[datetime] = Field(None, description="Filter from date")
    to_date: Optional[datetime] = Field(None, description="Filter to date")
    interviewer: Optional[str] = Field(None, description="Filter by interviewer name")


class StartInterviewRequest(BaseModel):
    """Request schema for starting an interview"""
    started_by: Optional[str] = Field(None, description="ID or name of who started the interview")


class FinishInterviewRequest(BaseModel):
    """Request schema for finishing an interview"""
    finished_by: Optional[str] = Field(None, description="ID or name of who finished the interview")
    score: Optional[float] = Field(None, ge=0, le=100, description="Final interview score")
    feedback: Optional[str] = Field(None, description="Final interview feedback")
    interviewer_notes: Optional[str] = Field(None, description="Final interviewer notes")
