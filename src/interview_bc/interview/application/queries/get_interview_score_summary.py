"""Get interview score summary query"""
from dataclasses import dataclass
from typing import Optional

from src.interview.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class InterviewScoreSummaryDto:
    interview_id: str
    total_answers: int
    scored_answers: int
    average_score: Optional[float]
    completion_percentage: float


@dataclass
class GetInterviewScoreSummaryQuery(Query):
    interview_id: str


class GetInterviewScoreSummaryQueryHandler(QueryHandler[GetInterviewScoreSummaryQuery, InterviewScoreSummaryDto]):
    def __init__(self, answer_repository: InterviewAnswerRepositoryInterface):
        self.answer_repository = answer_repository

    def handle(self, query: GetInterviewScoreSummaryQuery) -> InterviewScoreSummaryDto:
        total_answers = self.answer_repository.count_by_interview(query.interview_id)
        scored_answers = self.answer_repository.count_scored_by_interview(query.interview_id)
        average_score = self.answer_repository.get_average_score_by_interview(query.interview_id)

        completion_percentage = (scored_answers / total_answers * 100) if total_answers > 0 else 0

        return InterviewScoreSummaryDto(
            interview_id=query.interview_id,
            total_answers=total_answers,
            scored_answers=scored_answers,
            average_score=average_score,
            completion_percentage=completion_percentage
        )
