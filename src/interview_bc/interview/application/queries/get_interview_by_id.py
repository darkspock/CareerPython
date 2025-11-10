"""Get interview by id query"""
from dataclasses import dataclass

from src.interview.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetInterviewByIdQuery(Query):
    interview_id: str


class GetInterviewByIdQueryHandler(QueryHandler[GetInterviewByIdQuery, InterviewDto]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewByIdQuery) -> InterviewDto:
        interview = self.interview_repository.get_by_id(query.interview_id)
        if not interview:
            raise InterviewNotFoundException(f"Interview with id {query.interview_id} not found")

        return InterviewDto.from_entity(interview)
