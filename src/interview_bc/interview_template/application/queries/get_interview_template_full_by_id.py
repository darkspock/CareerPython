from typing import Optional, List

from src.interview_bc.interview_template.application.queries.dtos.interview_template_full_dto import (
    InterviewTemplateFullDto,
    InterviewTemplateSectionDto,
    InterviewTemplateQuestionDto
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_section_repository import \
    InterviewTemplateSectionRepository
from src.framework.application.query_bus import Query, QueryHandler


class GetInterviewTemplateFullByIdQuery(Query):
    def __init__(self, id: InterviewTemplateId):
        self.id = id
        self.handler = GetInterviewTemplateFullByIdQueryHandler


class GetInterviewTemplateFullByIdQueryHandler(
    QueryHandler[GetInterviewTemplateFullByIdQuery, Optional[InterviewTemplateFullDto]]):
    def __init__(
            self,
            interview_template_repository: InterviewTemplateRepository,
            interview_template_section_repository: InterviewTemplateSectionRepository,
            interview_template_question_repository: InterviewTemplateQuestionRepository
    ):
        self.interview_template_repository = interview_template_repository
        self.interview_template_section_repository = interview_template_section_repository
        self.interview_template_question_repository = interview_template_question_repository

    def handle(self, query: GetInterviewTemplateFullByIdQuery) -> Optional[InterviewTemplateFullDto]:
        # Get the main template
        interview_template = self.interview_template_repository.get_by_id(query.id)
        if not interview_template:
            return None

        # Get all sections for this template
        sections = self.interview_template_section_repository.get_by_template_id(query.id)

        # Sort sections by sort_order first, then recalculate sort_order to ensure consistency
        sections.sort(key=lambda s: s.sort_order)

        # Recalculate sort_order to ensure sequential ordering (0, 1, 2, 3...)
        needs_update = False
        for index, section in enumerate(sections):
            if section.sort_order != index:
                section.sort_order = index
                needs_update = True

        # If sort_order values were inconsistent, update them in the database
        if needs_update:
            for section in sections:
                self.interview_template_section_repository.update(section)

        # Build section DTOs with their questions
        section_dtos: List[InterviewTemplateSectionDto] = []
        for section in sections:
            # Get questions for this section
            questions = self.interview_template_question_repository.get_by_section_id(section.id)
            question_dtos = [InterviewTemplateQuestionDto.from_entity(q) for q in questions]

            # Create section DTO
            section_dto = InterviewTemplateSectionDto.from_entity(section, question_dtos)
            section_dtos.append(section_dto)

        # Create the full DTO
        return InterviewTemplateFullDto(
            id=interview_template.id,
            company_id=interview_template.company_id.value if interview_template.company_id else None,
            name=interview_template.name,
            intro=interview_template.intro,
            prompt=interview_template.prompt,
            goal=interview_template.goal,
            status=interview_template.status,
            template_type=interview_template.template_type,
            job_category=interview_template.job_category,
            tags=interview_template.tags or [],
            metadata=interview_template.metadata or {},
            sections=section_dtos,
            allow_ai_questions=interview_template.allow_ai_questions,
            legal_notice=interview_template.legal_notice,
            created_at=interview_template.metadata.get('created_at') if interview_template.metadata else None,
            updated_at=interview_template.metadata.get('updated_at') if interview_template.metadata else None,
        )
