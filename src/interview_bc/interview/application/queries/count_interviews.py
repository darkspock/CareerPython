"""Count interviews query"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum,
    InterviewProcessTypeEnum
)
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class CountInterviewsQuery(Query):
    """Query to count interviews with filters"""
    candidate_id: Optional[str] = None
    candidate_name: Optional[str] = None
    job_position_id: Optional[str] = None
    interview_type: Optional[InterviewTypeEnum] = None
    process_type: Optional[InterviewProcessTypeEnum] = None
    status: Optional[InterviewStatusEnum] = None
    required_role_id: Optional[str] = None
    interviewer_user_id: Optional[str] = None
    created_by: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    filter_by: Optional[str] = None
    has_scheduled_at_and_interviewers: bool = False


class CountInterviewsQueryHandler(QueryHandler[CountInterviewsQuery, int]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: CountInterviewsQuery) -> int:
        return self.interview_repository.count_by_filters(
            candidate_id=query.candidate_id,
            candidate_name=query.candidate_name,
            job_position_id=query.job_position_id,
            interview_type=query.interview_type,
            process_type=query.process_type,
            status=query.status,
            required_role_id=query.required_role_id,
            interviewer_user_id=query.interviewer_user_id,
            created_by=query.created_by,
            from_date=query.from_date,
            to_date=query.to_date,
            filter_by=query.filter_by,
            has_scheduled_at_and_interviewers=query.has_scheduled_at_and_interviewers
        )
