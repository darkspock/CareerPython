"""Get interview questions by token query"""
from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler, QueryBus
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateFullDto
from src.interview_bc.interview_template.application.queries.get_interview_template_full_by_id import \
    GetInterviewTemplateFullByIdQuery


@dataclass
class GetInterviewQuestionsByTokenQuery(Query):
    interview_id: str
    token: str


@dataclass
class InterviewQuestionsResponse:
    """Response with interview info and template questions"""
    interview_id: str
    interview_title: Optional[str]
    interview_description: Optional[str]
    template: Optional[InterviewTemplateFullDto]
    existing_answers: dict  # question_id -> answer_text mapping


class GetInterviewQuestionsByTokenQueryHandler(
    QueryHandler[GetInterviewQuestionsByTokenQuery, InterviewQuestionsResponse]):
    def __init__(
            self,
            interview_repository: InterviewRepositoryInterface,
            answer_repository: InterviewAnswerRepositoryInterface,
            query_bus: QueryBus
    ):
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.query_bus = query_bus

    def handle(self, query: GetInterviewQuestionsByTokenQuery) -> InterviewQuestionsResponse:
        # Get interview by token
        interview = self.interview_repository.get_by_token(query.interview_id, query.token)
        if not interview:
            raise InterviewNotFoundException(
                f"Interview with id {query.interview_id} not found or token is invalid/expired"
            )

        # Get template with questions if template_id exists
        template = None
        if interview.interview_template_id:
            template_query = GetInterviewTemplateFullByIdQuery(interview.interview_template_id)
            template = self.query_bus.query(template_query)

        # Get existing answers
        existing_answers_list = self.answer_repository.get_by_interview_id(query.interview_id)

        # Create mapping of question_id -> answer_text
        existing_answers = {}
        for answer in existing_answers_list:
            existing_answers[answer.question_id.value] = answer.answer_text

        return InterviewQuestionsResponse(
            interview_id=query.interview_id,
            interview_title=interview.title,
            interview_description=interview.description,
            template=template,
            existing_answers=existing_answers
        )
