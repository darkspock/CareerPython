from dataclasses import dataclass, field
from typing import Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateStatusEnum,
    InterviewTemplateTypeEnum,
    ScoringModeEnum
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class InterviewTemplate:
    id: InterviewTemplateId
    company_id: Optional[CompanyId]
    name: str
    intro: str  # short for interview
    prompt: str  # instructions for the interviewer
    goal: str  # what to achieve with this template
    status: InterviewTemplateStatusEnum
    template_type: InterviewTemplateTypeEnum
    job_category: Optional[JobCategoryEnum]
    allow_ai_questions: bool = False  # If True, AI can generate additional questions beyond the defined ones
    scoring_mode: Optional[ScoringModeEnum] = None  # Scoring mode: DISTANCE or ABSOLUTE (None = no scoring)
    legal_notice: Optional[str] = None  # Legal text displayed to users for compliance
    tags: Optional[list] = field(default_factory=list)
    metadata: Optional[dict] = field(default_factory=dict)

    @staticmethod
    def create(id: InterviewTemplateId, company_id: Optional[CompanyId], name: str, intro: str, prompt: str, goal: str,
               status: InterviewTemplateStatusEnum, template_type: InterviewTemplateTypeEnum,
               job_category: Optional[JobCategoryEnum],
               allow_ai_questions: bool = False,
               scoring_mode: Optional[ScoringModeEnum] = None,
               legal_notice: Optional[str] = None,
               tags: Optional[list] = None, metadata: Optional[dict] = None) -> 'InterviewTemplate':
        return InterviewTemplate(
            id=id,
            company_id=company_id,
            name=name,
            intro=intro,
            prompt=prompt,
            goal=goal,
            status=status,
            template_type=template_type,
            job_category=job_category,
            allow_ai_questions=allow_ai_questions,
            scoring_mode=scoring_mode,
            legal_notice=legal_notice,
            tags=tags if tags is not None else [],
            metadata=metadata if metadata is not None else {}
        )

    def update_details(self, company_id: Optional[CompanyId], name: str, status: InterviewTemplateStatusEnum,
                       template_type: InterviewTemplateTypeEnum, job_category: Optional[JobCategoryEnum],
                       allow_ai_questions: bool = False,
                       scoring_mode: Optional[ScoringModeEnum] = None,
                       legal_notice: Optional[str] = None
                       ) -> None:
        self.name = name
        self.company_id = company_id
        self.status = status
        self.template_type = template_type
        self.job_category = job_category
        self.allow_ai_questions = allow_ai_questions
        self.scoring_mode = scoring_mode
        self.legal_notice = legal_notice

    def enable(self) -> None:
        """Enable this interview template"""
        self.status = InterviewTemplateStatusEnum.ENABLED

    def disable(self) -> None:
        """Disable this interview template"""
        self.status = InterviewTemplateStatusEnum.DISABLED

    def publish(self) -> None:
        """Publish this interview template"""
        self.status = InterviewTemplateStatusEnum.ENABLED

    def draft(self) -> None:
        """Set this interview template to draft status"""
        self.status = InterviewTemplateStatusEnum.DRAFT
