from typing import Optional, List, Dict, Any

from pydantic import BaseModel, ConfigDict

from src.framework.domain.enums.job_category import JobCategoryEnum
from src.interview_bc.interview_template.application.queries.dtos.interview_template_dto import InterviewTemplateDto
from src.interview_bc.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateSectionDto, InterviewTemplateFullDto
from src.interview_bc.interview_template.application.queries.dtos.interview_template_list_dto import \
    InterviewTemplateListDto
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateTypeEnum,
    InterviewTemplateStatusEnum,
    InterviewTemplateSectionEnum,
    ScoringModeEnum
)


class InterviewTemplateBase(BaseModel):
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    type: InterviewTemplateTypeEnum
    job_category: Optional[JobCategoryEnum] = None
    allow_ai_questions: Optional[bool] = False
    scoring_mode: Optional[ScoringModeEnum] = None
    legal_notice: Optional[str] = None
    tags: Optional[List[str]] = None
    template_metadata: Optional[Dict[str, Any]] = None

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateCreate(InterviewTemplateBase):
    sections: Optional[List[Dict]] = None  # Accept sections as raw dict data

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplate(InterviewTemplateBase):
    id: str
    status: InterviewTemplateStatusEnum

    model_config = ConfigDict(from_attributes=True)


class InterviewTemplateResponse(InterviewTemplateBase):
    id: str
    status: InterviewTemplateStatusEnum
    company_id: Optional[str] = None  # Company that owns this template
    sections: Optional[List['InterviewTemplateSectionResponse']] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_dto(cls, dto: InterviewTemplateDto) -> 'InterviewTemplateResponse':
        """Convert DTO to Response schema"""
        return cls(
            id=dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
            name=dto.name,
            intro=dto.intro,
            prompt=dto.prompt,
            goal=dto.goal,
            type=dto.template_type,
            status=dto.status,
            company_id=dto.company_id.value if dto.company_id and hasattr(dto.company_id, 'value') else (
                str(dto.company_id) if dto.company_id else None),
            job_category=dto.job_category,
            allow_ai_questions=dto.allow_ai_questions,
            scoring_mode=dto.scoring_mode,
            legal_notice=dto.legal_notice,
            tags=dto.tags,
            template_metadata=dto.metadata
        )

    @classmethod
    def from_full_dto(cls, dto: InterviewTemplateFullDto) -> 'InterviewTemplateResponse':
        """Convert Full DTO to Response schema (including sections)"""
        sections = None
        if hasattr(dto, 'sections') and dto.sections:
            sections = [InterviewTemplateSectionResponse.from_dto(section_dto) for section_dto in dto.sections]

        return cls(
            id=dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
            name=dto.name,
            intro=dto.intro,
            prompt=dto.prompt,
            goal=dto.goal,
            type=dto.template_type,
            status=dto.status,
            company_id=dto.company_id,  # Already a string in FullDto
            job_category=dto.job_category,
            allow_ai_questions=dto.allow_ai_questions,
            scoring_mode=dto.scoring_mode,
            legal_notice=dto.legal_notice,
            tags=dto.tags,
            template_metadata=dto.metadata,
            sections=sections
        )

    @classmethod
    def from_list_dto(cls, dto: InterviewTemplateListDto) -> 'InterviewTemplateResponse':
        """Convert ListDTO to Response schema"""
        return cls(
            id=dto.id.value if hasattr(dto.id, 'value') else str(dto.id),
            name=dto.name,
            type=dto.template_type,
            status=dto.status,
            job_category=dto.job_category,
            tags=dto.tags,
            # Set defaults for fields not in ListDTO
            intro=None,
            prompt=None,
            goal=None,
            allow_ai_questions=False,
            legal_notice=None,
            template_metadata={}
        )


# Section models
class InterviewTemplateSectionBase(BaseModel):
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    section: Optional[InterviewTemplateSectionEnum] = None
    sort_order: int = 0
    allow_ai_questions: Optional[bool] = False
    allow_ai_override_questions: Optional[bool] = False
    legal_notice: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateSectionCreate(InterviewTemplateSectionBase):
    interview_template_id: str
    company_id: Optional[str] = None

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateSectionUpdate(InterviewTemplateSectionBase):
    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateSectionResponse(InterviewTemplateSectionBase):
    id: str
    interview_template_id: str
    status: str

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def from_dto(cls, dto: InterviewTemplateSectionDto) -> 'InterviewTemplateSectionResponse':
        """Convert section DTO to Response schema"""
        return cls(
            id=dto.id,
            interview_template_id=dto.interview_template_id,
            name=dto.name,
            intro=dto.intro,
            prompt=dto.prompt,
            goal=dto.goal,
            section=dto.section,
            sort_order=dto.sort_order,
            allow_ai_questions=dto.allow_ai_questions,
            allow_ai_override_questions=dto.allow_ai_override_questions,
            legal_notice=dto.legal_notice,
            status=dto.status.value
        )


# Question models
class InterviewTemplateQuestionBase(BaseModel):
    name: str
    description: str
    code: str
    sort_order: int
    allow_ai_followup: Optional[bool] = False
    legal_notice: Optional[str] = None
    scoring_values: Optional[List[Dict[str, Any]]] = None  # Array of {label: string, scoring: number}

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateQuestionCreate(InterviewTemplateQuestionBase):
    interview_template_section_id: str
    scope: str  # InterviewTemplateQuestionScopeEnum
    data_type: str  # InterviewTemplateQuestionDataTypeEnum

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateQuestionUpdate(InterviewTemplateQuestionBase):
    interview_template_section_id: str
    scope: str  # InterviewTemplateQuestionScopeEnum
    data_type: str  # InterviewTemplateQuestionDataTypeEnum

    model_config = ConfigDict(use_enum_values=True)


class InterviewTemplateQuestionResponse(InterviewTemplateQuestionBase):
    id: str
    interview_template_section_id: str
    scope: str
    data_type: str
    status: str
    scoring_values: Optional[List[Dict[str, Any]]] = None  # Array of {label: string, scoring: number}

    model_config = ConfigDict(from_attributes=True)
