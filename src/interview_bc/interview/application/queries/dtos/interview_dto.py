"""Interview DTO for application layer"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.candidate_bc.candidate.domain.value_objects import CandidateId
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.interview_bc.interview.domain.entities.interview import Interview
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass
class InterviewDto:
    id: InterviewId
    candidate_id: CandidateId
    job_position_id: Optional[JobPositionId]
    application_id: Optional[CandidateApplicationId]
    interview_template_id: Optional[InterviewTemplateId]
    workflow_stage_id: Optional[WorkflowStageId]
    interview_type: str
    status: str
    title: Optional[str]
    description: Optional[str]
    scheduled_at: Optional[datetime]
    started_at: Optional[datetime]
    finished_at: Optional[datetime]
    duration_minutes: Optional[int]
    interviewers: List[str]
    interviewer_notes: Optional[str]
    candidate_notes: Optional[str]
    score: Optional[float]
    feedback: Optional[str]
    free_answers: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @classmethod
    def from_entity(cls, entity: Interview) -> "InterviewDto":
        """Convert domain entity to DTO"""
        return cls(
            id=entity.id,
            candidate_id=entity.candidate_id,
            job_position_id=entity.job_position_id,
            application_id=entity.application_id,
            interview_template_id=entity.interview_template_id,
            workflow_stage_id=entity.workflow_stage_id,
            interview_type=entity.interview_type.value,
            status=entity.status.value,
            title=entity.title,
            description=entity.description,
            scheduled_at=entity.scheduled_at,
            started_at=entity.started_at,
            finished_at=entity.finished_at,
            duration_minutes=entity.duration_minutes,
            interviewers=entity.interviewers or [],
            interviewer_notes=entity.interviewer_notes,
            candidate_notes=entity.candidate_notes,
            score=entity.score,
            feedback=entity.feedback,
            free_answers=entity.free_answers,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
