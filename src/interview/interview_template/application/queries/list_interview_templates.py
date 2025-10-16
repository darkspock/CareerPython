from dataclasses import dataclass
from typing import List, Optional, Dict, Any

from src.interview.interview_template.application.queries.dtos.interview_template_list_dto import \
    InterviewTemplateListDto
from src.interview.interview_template.domain.enums import InterviewTemplateStatusEnum, InterviewTemplateTypeEnum, \
    InterviewTemplateSectionEnum
from src.interview.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.shared.application.query_bus import Query, QueryHandler
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListInterviewTemplatesQuery(Query):
    search_term: Optional[str] = None
    type: Optional[InterviewTemplateTypeEnum] = None
    status: Optional[InterviewTemplateStatusEnum] = None
    job_category: Optional[JobCategoryEnum] = None
    section: Optional[InterviewTemplateSectionEnum] = None
    page: Optional[int] = None
    page_size: Optional[int] = None


class ListInterviewTemplatesQueryHandler(QueryHandler[ListInterviewTemplatesQuery, List[InterviewTemplateListDto]]):
    def __init__(self, interview_template_repository: InterviewTemplateRepository):
        self.interview_template_repository = interview_template_repository

    def handle(self, query: ListInterviewTemplatesQuery) -> List[InterviewTemplateListDto]:
        # Build search criteria dictionary
        criteria: Dict[str, Any] = {}

        if query.search_term:
            criteria['text_search'] = query.search_term
        if query.type:
            criteria['type'] = query.type
        if query.status:
            criteria['status'] = query.status
        if query.job_category:
            criteria['job_category'] = query.job_category
        if query.section:
            criteria['section'] = query.section
        if query.page and query.page_size:
            criteria['offset'] = (query.page - 1) * query.page_size
            criteria['limit'] = query.page_size
        elif query.page_size:
            criteria['limit'] = query.page_size

        interview_templates = self.interview_template_repository.search(**criteria)

        # Convert domain entities to DTOs
        return [InterviewTemplateListDto.from_entity(template) for template in interview_templates]
