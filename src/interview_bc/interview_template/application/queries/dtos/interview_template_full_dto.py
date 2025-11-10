from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.interview.interview_template.domain import InterviewTemplateQuestion, InterviewTemplateSection
from src.interview.interview_template.domain.enums import (
    InterviewTemplateStatusEnum,
    InterviewTemplateTypeEnum, InterviewTemplateSectionEnum
)
from src.interview.interview_template.domain.enums.interview_template_question import (
    InterviewTemplateQuestionStatusEnum,
    InterviewTemplateQuestionDataTypeEnum,
    InterviewTemplateQuestionScopeEnum
)
from src.interview.interview_template.domain.enums.interview_template_section import InterviewTemplateSectionStatusEnum
from src.interview.interview_template.domain.value_objects import InterviewTemplateQuestionId, \
    InterviewTemplateSectionId, InterviewTemplateId
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class InterviewTemplateQuestionDto:
    """DTO for Interview Template Question with all properties"""
    id: InterviewTemplateQuestionId
    interview_template_section_id: InterviewTemplateSectionId
    sort_order: int
    name: str
    description: str
    data_type: InterviewTemplateQuestionDataTypeEnum
    scope: InterviewTemplateQuestionScopeEnum
    code: str
    status: InterviewTemplateQuestionStatusEnum
    allow_ai_followup: bool
    legal_notice: Optional[str]

    @classmethod
    def from_entity(cls, entity: InterviewTemplateQuestion) -> 'InterviewTemplateQuestionDto':
        """Convert domain entity to DTO"""
        return cls(
            id=entity.id,
            interview_template_section_id=entity.interview_template_section_id,
            sort_order=entity.sort_order,
            name=entity.name,
            description=entity.description,
            data_type=entity.data_type,
            scope=entity.scope,
            code=entity.code,
            status=entity.status,
            allow_ai_followup=entity.allow_ai_followup,
            legal_notice=entity.legal_notice
        )


@dataclass
class InterviewTemplateSectionDto:
    """DTO for Interview Template Section with all properties and questions"""
    id: str
    interview_template_id: str
    name: str
    intro: str
    prompt: str
    goal: str
    section: Optional[InterviewTemplateSectionEnum]
    sort_order: int
    status: InterviewTemplateSectionStatusEnum
    allow_ai_questions: bool
    allow_ai_override_questions: bool
    legal_notice: Optional[str]
    questions: List[InterviewTemplateQuestionDto]

    @classmethod
    def from_entity(cls, entity: InterviewTemplateSection,
                    questions: List[InterviewTemplateQuestionDto]) -> 'InterviewTemplateSectionDto':
        """Convert domain entity to DTO"""
        return cls(
            id=entity.id.value,
            interview_template_id=entity.interview_template_id.value,
            name=entity.name,
            intro=entity.intro,
            prompt=entity.prompt,
            goal=entity.goal,
            section=entity.section,
            sort_order=entity.sort_order,
            status=entity.status,
            allow_ai_questions=entity.allow_ai_questions,
            allow_ai_override_questions=entity.allow_ai_override_questions,
            legal_notice=entity.legal_notice,
            questions=questions
        )


@dataclass
class InterviewTemplateFullDto:
    """Complete DTO for Interview Template with all properties, sections and questions"""
    # Core template properties
    id: InterviewTemplateId
    company_id: Optional[str]
    name: str
    intro: str
    prompt: str
    goal: str
    status: InterviewTemplateStatusEnum
    template_type: InterviewTemplateTypeEnum
    job_category: Optional[JobCategoryEnum]
    allow_ai_questions: bool
    legal_notice: Optional[str]

    # Extended properties
    tags: List[str]
    metadata: Dict[str, Any]

    # Related entities - array of sections
    sections: List[InterviewTemplateSectionDto]

    # Timestamps (from metadata)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @property
    def total_questions(self) -> int:
        """Total number of questions across all sections"""
        return sum(len(section.questions) for section in self.sections)

    @property
    def enabled_questions_count(self) -> int:
        """Count of enabled questions across all sections"""
        return sum(
            len([q for q in section.questions if q.status == InterviewTemplateQuestionStatusEnum.ENABLED])
            for section in self.sections
        )

    @property
    def enabled_sections_count(self) -> int:
        """Count of enabled sections"""
        return len([s for s in self.sections if s.status == InterviewTemplateSectionStatusEnum.ENABLED])

    @property
    def is_complete(self) -> bool:
        """Check if template has at least one section with at least one question"""
        return any(len(section.questions) > 0 for section in self.sections)

    @property
    def is_ready_for_use(self) -> bool:
        """Check if template is enabled and has enabled sections with enabled questions"""
        return (
                self.status == InterviewTemplateStatusEnum.ENABLED and
                self.enabled_sections_count > 0 and
                self.enabled_questions_count > 0
        )
