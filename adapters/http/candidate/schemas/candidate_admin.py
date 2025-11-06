from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, Field, ConfigDict

from src.candidate.domain.enums import CandidateStatusEnum
from src.shared.domain.enums.job_category import JobCategoryEnum


class CandidateAdminResponse(BaseModel):
    id: str
    name: str
    email: str
    phone: Optional[str]
    city: Optional[str]
    country: Optional[str]
    status: CandidateStatusEnum
    job_category: Optional[JobCategoryEnum]
    expected_annual_salary: Optional[float]
    currency: Optional[str]
    date_of_birth: Optional[date]
    relocation: Optional[bool]
    work_modality: Optional[str]
    languages: Optional[List[str]]
    user_id: str
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)


class CandidateListResponse(BaseModel):
    candidates: List[CandidateAdminResponse]
    total_count: int
    has_more: bool


class CandidateStatsResponse(BaseModel):
    total_count: int
    active_count: int
    inactive_count: int
    pending_count: int
    approved_count: int
    rejected_count: int
    recent_count: int
    with_resume_count: int


class CandidateStatusUpdate(BaseModel):
    status: CandidateStatusEnum
    notes: Optional[str] = Field(None, max_length=1000)
