from typing import Optional

from src.interview.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateQuestionDto
from src.interview.interview_template.domain.value_objects import InterviewTemplateQuestionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.shared.application.query_bus import Query, QueryHandler


class GetInterviewTemplateQuestionByIdQuery(Query):
    def __init__(self, id: InterviewTemplateQuestionId):
        self.id = id
        self.handler = GetInterviewTemplateQuestionByIdQueryHandler


class GetInterviewTemplateQuestionByIdQueryHandler(
    QueryHandler[GetInterviewTemplateQuestionByIdQuery, Optional[InterviewTemplateQuestionDto]]):
    def __init__(self, interview_template_question_repository: InterviewTemplateQuestionRepository):
        self.interview_template_question_repository = interview_template_question_repository

    def handle(self, query: GetInterviewTemplateQuestionByIdQuery) -> Optional[InterviewTemplateQuestionDto]:
        interview_template_question = self.interview_template_question_repository.get_by_id(query.id)
        if interview_template_question:
            return InterviewTemplateQuestionDto.from_entity(interview_template_question)
        return None
