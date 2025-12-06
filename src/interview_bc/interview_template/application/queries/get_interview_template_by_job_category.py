from typing import Optional

from src.framework.application.query_bus import Query, QueryHandler
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.interview_bc.interview_template.application.queries.dtos import (
    InterviewTemplateFullDto,
    InterviewTemplateSectionDto,
    InterviewTemplateQuestionDto
)
from src.interview_bc.interview_template.domain.enums.interview_template_question import \
    InterviewTemplateQuestionStatusEnum
from src.interview_bc.interview_template.domain.enums.interview_template_section import \
    InterviewTemplateSectionStatusEnum
from src.interview_bc.interview_template.infrastructure.repositories import InterviewTemplateSectionRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_repository import \
    InterviewTemplateRepository


class GetInterviewTemplateByJobCategoryQuery(Query):
    def __init__(self, job_category: Optional[JobCategoryEnum] = None, preview: bool = False):
        self.job_category = job_category
        self.preview = preview  # If True, don't filter by status (show all sections and questions)


class GetInterviewTemplateByJobCategoryQueryHandler(
    QueryHandler[GetInterviewTemplateByJobCategoryQuery, Optional[InterviewTemplateFullDto]]):
    def __init__(self, interview_template_repository: InterviewTemplateRepository,
                 interview_template_question_repository: InterviewTemplateQuestionRepository,
                 interview_template_section_repository: InterviewTemplateSectionRepository):
        self.interview_template_repository = interview_template_repository
        self.interview_template_question_repository = interview_template_question_repository
        self.interview_template_section_repository = interview_template_section_repository

    def handle(self, query: GetInterviewTemplateByJobCategoryQuery) -> Optional[InterviewTemplateFullDto]:
        """
        Returns template for the specified job category, or base template if no category-specific template exists.

        Args:
            query: Contains job_category and preview flag
                - job_category: Filter for specific job category (None for base template)
                - preview: If True, includes ALL sections and questions regardless of status (DRAFT, ENABLED, DISABLED)
                          If False, only includes ENABLED sections and questions
        """
        template = None

        # 1. If job_category is specified, try to get category-specific template first
        if query.job_category:
            category_templates = self.interview_template_repository.get_by_job_category(query.job_category)
            if category_templates:
                template = category_templates[0]

        # 2. If no category template found, get base template (job_category=null)
        if not template:
            base_templates = self.interview_template_repository.get_by_job_category(None)
            if base_templates:
                template = base_templates[0]

        # If no template found, return None
        if not template:
            return None

        # Get sections from the selected template
        sections = self.interview_template_section_repository.get_by_template_id(template.id)

        # Filter sections by status only if not in preview mode
        if query.preview:
            sections_to_process = sections
        else:
            sections_to_process = [s for s in sections if s.status == InterviewTemplateSectionStatusEnum.ENABLED]

        # Convert to DTOs
        section_dtos = []
        for section in sections_to_process:
            # Get questions for this section
            questions = self.interview_template_question_repository.get_by_section_id(section.id)

            # Filter questions by status only if not in preview mode
            if query.preview:
                final_questions = questions
            else:
                final_questions = [q for q in questions if q.status == InterviewTemplateQuestionStatusEnum.ENABLED]

            question_dtos = [
                InterviewTemplateQuestionDto(
                    id=q.id,
                    interview_template_section_id=q.interview_template_section_id,
                    sort_order=q.sort_order,
                    name=q.name,
                    description=q.description,
                    data_type=q.data_type,
                    scope=q.scope,
                    code=q.code,
                    status=q.status,
                    allow_ai_followup=q.allow_ai_followup,
                    legal_notice=q.legal_notice
                ) for q in final_questions
            ]

            section_dto = InterviewTemplateSectionDto(
                id=section.id.value,
                interview_template_id=section.interview_template_id.value,
                name=section.name,
                intro=section.intro,
                prompt=section.prompt,
                goal=section.goal,
                section=section.section,
                status=section.status,
                questions=question_dtos,
                sort_order=section.sort_order,
                allow_ai_questions=section.allow_ai_questions,
                allow_ai_override_questions=section.allow_ai_override_questions,
                legal_notice=section.legal_notice
            )
            section_dtos.append(section_dto)

        # Create the full DTO using the selected template data
        return InterviewTemplateFullDto(
            id=template.id,
            company_id=template.company_id.value if template.company_id else None,
            name=template.name,
            intro=template.intro,
            prompt=template.prompt,
            goal=template.goal,
            status=template.status,
            template_type=template.template_type,
            job_category=template.job_category,
            tags=template.tags or [],
            metadata=template.metadata or {},
            allow_ai_questions=template.allow_ai_questions,
            use_conversational_mode=template.use_conversational_mode,
            scoring_mode=template.scoring_mode,
            legal_notice=template.legal_notice,
            created_at=template.metadata.get('created_at') if template.metadata else None,
            updated_at=template.metadata.get('updated_at') if template.metadata else None,
            sections=section_dtos
        )
