"""Get interviews by date range query for calendar"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetInterviewsByDateRangeQuery(Query):
    """Query to get interviews within a date range for calendar view"""
    from_date: datetime
    to_date: datetime
    company_id: Optional[str] = None  # Filter by company
    filter_by: Optional[str] = None  # 'scheduled' or 'deadline' - which date field to filter


class GetInterviewsByDateRangeQueryHandler(QueryHandler[GetInterviewsByDateRangeQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewsByDateRangeQuery) -> List[InterviewDto]:
        """Get interviews within date range"""
        interviews = self.interview_repository.find_by_filters(
            from_date=query.from_date,
            to_date=query.to_date,
            filter_by=query.filter_by,
            limit=10000  # Get all interviews in the range
        )
        
        # Filter by company if needed
        # TODO: Add company filtering to repository if needed
        
        return [InterviewDto.from_entity(interview) for interview in interviews]

