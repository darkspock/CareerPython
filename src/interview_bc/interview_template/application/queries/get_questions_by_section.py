from typing import List

from src.interview_bc.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateQuestionDto
from src.interview_bc.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.framework.application.query_bus import Query, QueryHandler


class GetQuestionsBySectionQuery(Query):
    def __init__(self, section_id: InterviewTemplateSectionId):
        self.section_id = section_id
        self.handler = GetQuestionsBySectionQueryHandler


class GetQuestionsBySectionQueryHandler(QueryHandler[GetQuestionsBySectionQuery, List[InterviewTemplateQuestionDto]]):
    def __init__(self, interview_template_question_repository: InterviewTemplateQuestionRepository):
        self.interview_template_question_repository = interview_template_question_repository

    def handle(self, query: GetQuestionsBySectionQuery) -> List[InterviewTemplateQuestionDto]:
        # Get all questions for this section
        questions = self.interview_template_question_repository.get_by_section_id(query.section_id)

        # Sort questions by sort_order
        questions.sort(key=lambda q: q.sort_order)

        # Convert to DTOs
        return [InterviewTemplateQuestionDto.from_entity(question) for question in questions]
