"""Get interview answer by id query"""
from dataclasses import dataclass

from src.interview.interview.application.queries.dtos.interview_answer_dto import InterviewAnswerDto
from src.interview.interview.domain.exceptions.interview_answer_exceptions import InterviewAnswerNotFoundException
from src.interview.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetInterviewAnswerByIdQuery(Query):
    answer_id: str


class GetInterviewAnswerByIdQueryHandler(QueryHandler[GetInterviewAnswerByIdQuery, InterviewAnswerDto]):
    def __init__(self, answer_repository: InterviewAnswerRepositoryInterface):
        self.answer_repository = answer_repository

    def handle(self, query: GetInterviewAnswerByIdQuery) -> InterviewAnswerDto:
        answer = self.answer_repository.get_by_id(query.answer_id)
        if not answer:
            raise InterviewAnswerNotFoundException(f"Interview answer with id {query.answer_id} not found")

        return InterviewAnswerDto.from_entity(answer)
