"""Get overdue interviews query"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class GetOverdueInterviewsQuery(Query):
    """Query to get interviews that have passed their deadline"""
    company_id: Optional[str] = None  # Filter by company


class GetOverdueInterviewsQueryHandler(QueryHandler[GetOverdueInterviewsQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetOverdueInterviewsQuery) -> List[InterviewDto]:
        """Get overdue interviews (deadline_date < now and not finished)"""

        now = datetime.utcnow()

        # Get all interviews and filter for overdue ones
        # TODO: Add repository method for overdue interviews if needed
        all_interviews = self.interview_repository.find_by_filters(limit=10000)

        overdue_interviews = [
            interview for interview in all_interviews
            if interview.deadline_date
               and interview.deadline_date < now
               and not interview.finished_at
        ]

        # Sort by deadline_date (most overdue first)
        overdue_interviews.sort(key=lambda x: x.deadline_date or datetime.min)

        return [InterviewDto.from_entity(interview) for interview in overdue_interviews]
