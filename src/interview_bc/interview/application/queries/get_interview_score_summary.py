"""Get interview score summary query"""
from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview.application.services.interview_score_calculator import InterviewScoreCalculator
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface


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
    def __init__(
            self,
            answer_repository: InterviewAnswerRepositoryInterface,
            interview_repository: InterviewRepositoryInterface,
            template_repository: InterviewTemplateRepositoryInterface
    ):
        self.answer_repository = answer_repository
        self.interview_repository = interview_repository
        self.template_repository = template_repository

    def handle(self, query: GetInterviewScoreSummaryQuery) -> InterviewScoreSummaryDto:
        total_answers = self.answer_repository.count_by_interview(query.interview_id)
        scored_answers = self.answer_repository.count_scored_by_interview(query.interview_id)

        # Get interview to check template and scoring mode
        interview = self.interview_repository.get_by_id(query.interview_id)
        scoring_mode = None
        if interview and interview.interview_template_id:
            template = self.template_repository.get_by_id(interview.interview_template_id)
            if template:
                scoring_mode = template.scoring_mode

        # Get all answer scores
        answers = self.answer_repository.get_by_interview_id(query.interview_id)
        answer_scores = [answer.score for answer in answers if answer.score is not None]

        # Calculate average score based on scoring mode
        if answer_scores:
            average_score = InterviewScoreCalculator.calculate_score(answer_scores, scoring_mode)
        else:
            average_score = None

        completion_percentage = (scored_answers / total_answers * 100) if total_answers > 0 else 0

        return InterviewScoreSummaryDto(
            interview_id=query.interview_id,
            total_answers=total_answers,
            scored_answers=scored_answers,
            average_score=average_score,
            completion_percentage=completion_percentage
        )
