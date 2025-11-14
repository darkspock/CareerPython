from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.interview_bc.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateQuestionDto
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateSectionId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository


class ListInterviewTemplateQuestionsQuery(Query):
    def __init__(self, interview_template_section_id: InterviewTemplateSectionId):
        self.interview_template_section_id = interview_template_section_id
        self.handler = ListInterviewTemplateQuestionsQueryHandler


class ListInterviewTemplateQuestionsQueryHandler(
    QueryHandler[ListInterviewTemplateQuestionsQuery, List[InterviewTemplateQuestionDto]]):
    def __init__(self, interview_template_question_repository: InterviewTemplateQuestionRepository):
        self.interview_template_question_repository = interview_template_question_repository

    def handle(self, query: ListInterviewTemplateQuestionsQuery) -> List[InterviewTemplateQuestionDto]:
        interview_template_questions = self.interview_template_question_repository.get_all(
            interview_template_section_id=query.interview_template_section_id)
        return [InterviewTemplateQuestionDto.from_entity(question) for question in interview_template_questions]
