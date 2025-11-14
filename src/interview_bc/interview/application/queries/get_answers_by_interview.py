"""Get answers by interview query"""
from dataclasses import dataclass
from typing import List

from src.interview_bc.interview.application.queries.dtos.interview_answer_dto import InterviewAnswerDto
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetAnswersByInterviewQuery(Query):
    interview_id: str


class GetAnswersByInterviewQueryHandler(QueryHandler[GetAnswersByInterviewQuery, List[InterviewAnswerDto]]):
    def __init__(self, answer_repository: InterviewAnswerRepositoryInterface):
        self.answer_repository = answer_repository

    def handle(self, query: GetAnswersByInterviewQuery) -> List[InterviewAnswerDto]:
        answers = self.answer_repository.get_by_interview_id(query.interview_id)
        return [InterviewAnswerDto.from_entity(answer) for answer in answers]
