"""Get interviews by candidate query"""
from dataclasses import dataclass
from typing import List

from src.interview.interview.application.queries.dtos.interview_dto import InterviewDto
from src.interview.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetInterviewsByCandidateQuery(Query):
    candidate_id: str


class GetInterviewsByCandidateQueryHandler(QueryHandler[GetInterviewsByCandidateQuery, List[InterviewDto]]):
    def __init__(self, interview_repository: InterviewRepositoryInterface):
        self.interview_repository = interview_repository

    def handle(self, query: GetInterviewsByCandidateQuery) -> List[InterviewDto]:
        interviews = self.interview_repository.get_by_candidate_id(query.candidate_id)
        return [InterviewDto.from_entity(interview) for interview in interviews]
