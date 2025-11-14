"""Get interview by token query"""
from dataclasses import dataclass

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class GetInterviewByTokenQuery(Query):
    interview_id: str
    token: str


class GetInterviewByTokenQueryHandler(QueryHandler[GetInterviewByTokenQuery, InterviewDto]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewByTokenQuery) -> InterviewDto:
        interview = self.interview_repository.get_by_token(query.interview_id, query.token)
        if not interview:
            raise InterviewNotFoundException(
                f"Interview with id {query.interview_id} not found or token is invalid/expired"
            )

        return InterviewDto.from_entity(interview)
