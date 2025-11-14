from dataclasses import dataclass
from typing import Optional, List

from src.interview_bc.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateStatusEnum,
    InterviewTemplateTypeEnum
)
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class InterviewTemplateListDto:
    """Simplified DTO for Interview Template lists - contains only essential fields"""
    id: InterviewTemplateId
    name: str
    status: InterviewTemplateStatusEnum
    template_type: InterviewTemplateTypeEnum
    job_category: Optional[JobCategoryEnum]
    tags: List[str]

    @classmethod
    def from_entity(cls, entity: InterviewTemplate) -> 'InterviewTemplateListDto':
        """Convert domain entity to list DTO"""
        return cls(
            id=entity.id,
            name=entity.name,
            status=entity.status,
            template_type=entity.template_type,
            job_category=entity.job_category,
            tags=entity.tags or []
        )
