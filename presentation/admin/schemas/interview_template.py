from pydantic import BaseModel
from typing import Optional, List, Dict, Any

from src.interview.interview_template.application.queries.dtos.interview_template_dto import InterviewTemplateDto
from src.interview.interview_template.application.queries.dtos.interview_template_list_dto import \
    InterviewTemplateListDto
from src.interview.interview_template.application.queries.dtos.interview_template_full_dto import \
    InterviewTemplateSectionDto, InterviewTemplateFullDto
from src.interview.interview_template.domain.enums import InterviewTemplateTypeEnum, InterviewTemplateStatusEnum, InterviewTemplateSectionEnum
from src.interview.interview_template.domain.value_objects import InterviewTemplateId
from src.shared.domain.enums.job_category import JobCategoryEnum
from src.shared.infrastructure.helpers.mixed_helper import MixedHelper


class InterviewTemplateBase(BaseModel):
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    type: InterviewTemplateTypeEnum
    job_category: Optional[JobCategoryEnum] = None
    section: Optional[InterviewTemplateSectionEnum] = None
    tags: Optional[List[str]] = None
    template_metadata: Optional[Dict[str, Any]] = None

    class Config:
        use_enum_values = True


class InterviewTemplateCreate(InterviewTemplateBase):
    sections: Optional[List[Dict]] = None  # Accept sections as raw dict data

    class Config:
        use_enum_values = True


class InterviewTemplate(InterviewTemplateBase):
    id: str
    status: InterviewTemplateStatusEnum

    class Config:
        from_attributes = True


class InterviewTemplateResponse(InterviewTemplateBase):
    id: InterviewTemplateId
    status: InterviewTemplateStatusEnum
    sections: Optional[List['InterviewTemplateSectionResponse']] = None

    class Config:
        from_attributes = True

    @classmethod
    def from_dto(cls, dto: InterviewTemplateDto) -> 'InterviewTemplateResponse':
        """Convert DTO to Response schema"""
        return cls(
            id=dto.id,
            name=dto.name,
            intro=dto.intro,
            prompt=dto.prompt,
            goal=dto.goal,
            type=dto.template_type,
            status=dto.status,
            job_category=dto.job_category,
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
            id=dto.id,
            name=dto.name,
            intro=dto.intro,
            prompt=dto.prompt,
            goal=dto.goal,
            type=dto.template_type,
            status=dto.status,
            job_category=dto.job_category,
            tags=dto.tags,
            template_metadata=dto.metadata,
            sections=sections
        )

    @classmethod
    def from_list_dto(cls, dto: InterviewTemplateListDto) -> 'InterviewTemplateResponse':
        """Convert ListDTO to Response schema"""
        return cls(
            id=dto.id,
            name=dto.name,
            type=dto.template_type,
            status=dto.status,
            job_category=dto.job_category,
            tags=dto.tags,
            # Set defaults for fields not in ListDTO
            intro=None,
            prompt=None,
            goal=None,
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

    class Config:
        use_enum_values = True


class InterviewTemplateSectionCreate(InterviewTemplateSectionBase):
    interview_template_id: str
    company_id: Optional[str] = None

    class Config:
        use_enum_values = True


class InterviewTemplateSectionUpdate(InterviewTemplateSectionBase):
    class Config:
        use_enum_values = True


class InterviewTemplateSectionResponse(InterviewTemplateSectionBase):
    id: str
    interview_template_id: str
    status: str

    class Config:
        from_attributes = True

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
            status=dto.status.value
        )


# Question models
class InterviewTemplateQuestionBase(BaseModel):
    name: str
    description: str
    code: str
    sort_order: int

    class Config:
        use_enum_values = True


class InterviewTemplateQuestionCreate(InterviewTemplateQuestionBase):
    interview_template_section_id: str
    scope: str  # InterviewTemplateQuestionScopeEnum
    data_type: str  # InterviewTemplateQuestionDataTypeEnum

    class Config:
        use_enum_values = True


class InterviewTemplateQuestionUpdate(InterviewTemplateQuestionBase):
    interview_template_section_id: str
    scope: str   # InterviewTemplateQuestionScopeEnum
    data_type: str  # InterviewTemplateQuestionDataTypeEnum

    class Config:
        use_enum_values = True


class InterviewTemplateQuestionResponse(InterviewTemplateQuestionBase):
    id: str
    interview_template_section_id: str
    scope: str
    data_type: str
    status: str

    class Config:
        from_attributes = True
