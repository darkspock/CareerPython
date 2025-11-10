"""List interviews query"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.domain.enums.interview_enums import InterviewStatusEnum, InterviewTypeEnum
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class ListInterviewsQuery(Query):
    candidate_id: Optional[str] = None
    job_position_id: Optional[str] = None
    interview_type: Optional[str] = None
    status: Optional[str] = None
    created_by: Optional[str] = None
    from_date: Optional[datetime] = None
    to_date: Optional[datetime] = None
    limit: int = 50
    offset: int = 0


class ListInterviewsQueryHandler(QueryHandler[ListInterviewsQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: ListInterviewsQuery) -> List[InterviewDto]:
        # Convert string enums to actual enum values
        interview_type = None
        if query.interview_type:
            interview_type = InterviewTypeEnum(query.interview_type)

        status = None
        if query.status:
            status = InterviewStatusEnum(query.status)

        interviews = self.interview_repository.find_by_filters(
            candidate_id=query.candidate_id,
            job_position_id=query.job_position_id,
            interview_type=interview_type,
            status=status,
            created_by=query.created_by,
            from_date=query.from_date,
            to_date=query.to_date,
            limit=query.limit,
            offset=query.offset
        )

        return [InterviewDto.from_entity(interview) for interview in interviews]
