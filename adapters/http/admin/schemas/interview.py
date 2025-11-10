from pydantic import BaseModel
from datetime import datetime
from typing import Optional

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.company.domain.value_objects import CompanyId
from src.interview.interview.domain.enums.interview_enums import InterviewStatusEnum, InterviewTypeEnum
from src.interview.interview_template.domain.value_objects import InterviewTemplateId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId


class InterviewBase(BaseModel):
    candidate_id: CandidateId
    company_id: Optional[CompanyId]
    job_post_id: Optional[JobPositionId]
    template_id: InterviewTemplateId
    status: InterviewStatusEnum
    interview_type: InterviewTypeEnum
    created_at: datetime
    updated_at: datetime
    completed_at: Optional[datetime]

    class Config:
        use_enum_values = True


class InterviewCreate(InterviewBase):
    id: str


class Interview(InterviewBase):
    id: str

    class Config:
        from_attributes = True


class InterviewResponse(InterviewBase):
    id: str

    class Config:
        from_attributes = True
