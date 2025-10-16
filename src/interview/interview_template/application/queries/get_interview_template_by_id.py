from typing import Optional

from src.interview.interview_template.application.queries.dtos.interview_template_dto import InterviewTemplateDto
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.shared.application.query_bus import Query, QueryHandler


class GetInterviewTemplateByIdQuery(Query):
    def __init__(self, id: InterviewTemplateId):
        self.id = id
        self.handler = GetInterviewTemplateByIdQueryHandler


class GetInterviewTemplateByIdQueryHandler(QueryHandler[GetInterviewTemplateByIdQuery, Optional[InterviewTemplateDto]]):
    def __init__(self, interview_template_repository: InterviewTemplateRepository):
        self.interview_template_repository = interview_template_repository

    def handle(self, query: GetInterviewTemplateByIdQuery) -> Optional[InterviewTemplateDto]:
        interview_template = self.interview_template_repository.get_by_id(query.id)
        if interview_template:
            return InterviewTemplateDto.from_entity(interview_template)
        return None
