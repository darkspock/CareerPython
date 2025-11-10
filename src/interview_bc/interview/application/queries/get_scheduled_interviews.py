"""Get scheduled interviews query"""
from dataclasses import dataclass
from datetime import datetime
from typing import List

from src.interview.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetScheduledInterviewsQuery(Query):
    from_date: datetime
    to_date: datetime


class GetScheduledInterviewsQueryHandler(QueryHandler[GetScheduledInterviewsQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetScheduledInterviewsQuery) -> List[InterviewDto]:
        interviews = self.interview_repository.get_scheduled_interviews(
            query.from_date,
            query.to_date
        )
        return [InterviewDto.from_entity(interview) for interview in interviews]
