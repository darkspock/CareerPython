from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, Dict, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.interview_bc.interview_template.domain.entities.interview_template import InterviewTemplate
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateStatusEnum,
    InterviewTemplateTypeEnum,
    ScoringModeEnum
)
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class InterviewTemplateDto:
    """Basic DTO for Interview Template - used by simple queries"""
    # Core template properties
    id: InterviewTemplateId
    company_id: Optional[CompanyId]
    name: str
    intro: str
    prompt: str
    goal: str
    status: InterviewTemplateStatusEnum
    template_type: InterviewTemplateTypeEnum
    job_category: Optional[JobCategoryEnum]
    allow_ai_questions: bool
    scoring_mode: Optional[ScoringModeEnum]
    legal_notice: Optional[str]

    # Extended properties
    tags: List[str]
    metadata: Dict[str, Any]

    # Timestamps (from metadata)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    @classmethod
    def from_entity(cls, entity: InterviewTemplate) -> 'InterviewTemplateDto':
        """Convert domain entity to DTO"""
        return cls(
            id=entity.id,
            company_id=entity.company_id,
            name=entity.name,
            intro=entity.intro,
            prompt=entity.prompt,
            goal=entity.goal,
            status=entity.status,
            template_type=entity.template_type,
            job_category=entity.job_category,
            allow_ai_questions=entity.allow_ai_questions,
            scoring_mode=entity.scoring_mode,
            legal_notice=entity.legal_notice,
            tags=entity.tags or [],
            metadata=entity.metadata or {},
            created_at=entity.metadata.get('created_at') if entity.metadata else None,
            updated_at=entity.metadata.get('updated_at') if entity.metadata else None,
        )
