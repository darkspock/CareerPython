"""Get interview full by ID query - returns interview with all denormalized data"""
from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_list_dto import InterviewListDto
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class GetInterviewFullByIdQuery(Query):
    """Query to get a single interview with all denormalized data (candidate, job position, etc.)"""
    interview_id: str


class GetInterviewFullByIdQueryHandler(QueryHandler[GetInterviewFullByIdQuery, Optional[InterviewListDto]]):
    """Handler for GetInterviewFullByIdQuery"""

    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewFullByIdQuery) -> Optional[InterviewListDto]:
        """Get interview with all joined data by ID"""
        read_model = self.interview_repository.get_by_id_with_joins(query.interview_id)
        if read_model:
            return InterviewListDto.from_read_model(read_model)
        return None
