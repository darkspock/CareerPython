from datetime import datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, Field

from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum


class JobApplicationResponse(BaseModel):
    id: str
    user_id: str
    candidate_id: str
    job_title: str
    company_name: str
    job_description: str
    job_url: Optional[str]
    tailored_resume: str
    cover_letter: str
    key_matches: List[str]
    suggestions: List[str]
    status: ApplicationStatusEnum
    created_at: datetime
    updated_at: datetime
    applied_at: Optional[datetime]
    metadata: Dict[str, Any] = Field(default_factory=dict)

    class Config:
        from_attributes = True


class CandidateJobApplicationSummary(BaseModel):
    id: str
    job_title: str
    company_name: str
    status: ApplicationStatusEnum
    created_at: datetime
    updated_at: Optional[datetime]
    applied_at: Optional[datetime]
    has_customized_content: bool

    class Config:
        from_attributes = True


class CandidateJobApplicationHistoryResponse(BaseModel):
    candidate_id: str
    total_applications: int
    draft_applications: int
    applied_applications: int
    completed_applications: int
    success_rate_percentage: float
    latest_application_date: Optional[datetime]
    applications: List[CandidateJobApplicationSummary]
    application_trends: Dict[str, Any]

    class Config:
        from_attributes = True


class CandidateJobApplicationStatsResponse(BaseModel):
    candidate_id: str
    period_days: int
    total_applications: int
    draft_applications: int
    applied_applications: int
    completed_applications: int
    recent_applications_count: int
    success_rate_percentage: float
    companies_applied_to: int
    most_applied_categories: List[str]
    application_frequency: str  # 'high', 'medium', 'low'
    recommendations: List[str]

    class Config:
        from_attributes = True


class JobApplicationListFilters(BaseModel):
    status: Optional[ApplicationStatusEnum] = None
    company_name: Optional[str] = None
    job_title: Optional[str] = None
    limit: Optional[int] = Field(None, ge=1, le=100)
    days_back: int = Field(default=365, ge=1, le=1095)  # Max 3 years
