from dataclasses import dataclass, field
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.interview.interview_template.domain.enums import InterviewTemplateStatusEnum, InterviewTemplateTypeEnum
from src.interview.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.shared.domain.enums.job_category import JobCategoryEnum


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
    tags: Optional[list] = field(default_factory=list)
    metadata: Optional[dict] = field(default_factory=dict)

    @staticmethod
    def create(id: InterviewTemplateId, company_id: Optional[CompanyId], name: str, intro: str, prompt: str, goal: str,
               status: InterviewTemplateStatusEnum, template_type: InterviewTemplateTypeEnum,
               job_category: Optional[JobCategoryEnum],
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
            tags=tags if tags is not None else [],
            metadata=metadata if metadata is not None else {}
        )

    def update_details(self, company_id: Optional[CompanyId], name: str, status: InterviewTemplateStatusEnum,
                       template_type: InterviewTemplateTypeEnum, job_category: Optional[JobCategoryEnum],
                       ) -> None:
        self.name = name
        self.company_id = company_id
        self.status = status
        self.template_type = template_type
        self.job_category = job_category

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
