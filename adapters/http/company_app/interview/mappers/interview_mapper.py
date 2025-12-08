"""Interview Mapper - Converts DTOs to Response schemas"""
from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING

from core.config import settings
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.application.queries.dtos.interview_list_dto import InterviewListDto
from src.interview_bc.interview.application.queries.dtos.interview_statistics_dto import InterviewStatisticsDto
from src.interview_bc.interview.application.queries.get_interview_score_summary import InterviewScoreSummaryDto

if TYPE_CHECKING:
    from adapters.http.company_app.interview.schemas.interview_management import (
        InterviewFullResource, InterviewResource, InterviewStatsResource, InterviewScoreSummaryResource
    )


class InterviewMapper:
    """Mapper for converting interview DTOs to response schemas"""

    @staticmethod
    def _generate_shareable_link(interview_id: str, link_token: Optional[str]) -> Optional[str]:
        """Generate shareable link for interview"""
        if not link_token:
            return None
        return f"{settings.FRONTEND_URL}/interviews/{interview_id}/access?token={link_token}"

    @classmethod
    def list_dto_to_full_response(cls, dto: InterviewListDto) -> "InterviewFullResource":
        """Convert InterviewListDto to InterviewFullResource"""
        from adapters.http.company_app.interview.schemas.interview_management import InterviewFullResource

        return InterviewFullResource(
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

    @classmethod
    def list_dtos_to_full_responses(cls, dtos: List[InterviewListDto]) -> List["InterviewFullResource"]:
        """Convert list of InterviewListDto to list of InterviewFullResource"""
        return [cls.list_dto_to_full_response(dto) for dto in dtos]

    @classmethod
    def dto_to_resource(cls, dto: InterviewDto) -> "InterviewResource":
        """Convert InterviewDto to InterviewResource (only interview fields, no denormalized data)"""
        from adapters.http.company_app.interview.schemas.interview_management import InterviewResource

        return InterviewResource(
            id=dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
            candidate_id=dto.candidate_id.value if hasattr(dto.candidate_id, 'value') else str(dto.candidate_id),
            required_roles=dto.required_roles or [],
            job_position_id=dto.job_position_id.value if dto.job_position_id and hasattr(dto.job_position_id,
                                                                                         'value') else (
                str(dto.job_position_id) if dto.job_position_id else None),
            application_id=dto.application_id.value if dto.application_id and hasattr(dto.application_id,
                                                                                      'value') else (
                str(dto.application_id) if dto.application_id else None),
            interview_template_id=dto.interview_template_id.value if dto.interview_template_id and hasattr(
                dto.interview_template_id, 'value') else (
                str(dto.interview_template_id) if dto.interview_template_id else None),
            workflow_stage_id=dto.workflow_stage_id.value if dto.workflow_stage_id and hasattr(dto.workflow_stage_id,
                                                                                               'value') else (
                str(dto.workflow_stage_id) if dto.workflow_stage_id else None),
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
            interviewers=dto.interviewers or [],
            interviewer_notes=dto.interviewer_notes,
            candidate_notes=dto.candidate_notes,
            score=dto.score,
            feedback=dto.feedback,
            free_answers=dto.free_answers,
            link_token=dto.link_token,
            link_expires_at=dto.link_expires_at,
            shareable_link=cls._generate_shareable_link(
                dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
                dto.link_token
            ) if dto.link_token else None,
            is_incomplete=dto.is_incomplete,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )

    @classmethod
    def stats_dto_to_response(cls, dto: InterviewStatisticsDto) -> "InterviewStatsResource":
        """Convert InterviewStatisticsDto to InterviewStatsResource"""
        from adapters.http.company_app.interview.schemas.interview_management import InterviewStatsResource

        return InterviewStatsResource(
            pending_to_plan=dto.pending_to_plan,
            planned=dto.planned,
            in_progress=dto.in_progress,
            recently_finished=dto.recently_finished,
            overdue=dto.overdue,
            pending_feedback=dto.pending_feedback
        )

    @classmethod
    def score_summary_dto_to_response(cls, dto: InterviewScoreSummaryDto) -> "InterviewScoreSummaryResource":
        """Convert InterviewScoreSummaryDto to InterviewScoreSummaryResource"""
        from adapters.http.company_app.interview.schemas.interview_management import InterviewScoreSummaryResource

        return InterviewScoreSummaryResource(
            interview_id=dto.interview_id,
            total_answers=dto.total_answers,
            scored_answers=dto.scored_answers,
            average_score=dto.average_score,
            completion_percentage=dto.completion_percentage
        )
