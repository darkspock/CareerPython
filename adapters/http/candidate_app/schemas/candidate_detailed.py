from datetime import datetime, date
from typing import Optional, List

from pydantic import BaseModel, ConfigDict

from src.candidate_bc.candidate.domain.enums import CandidateStatusEnum
from src.framework.domain.enums.job_category import JobCategoryEnum


class CandidateExperienceResponse(BaseModel):
    id: str
    company_name: str
    position: str
    description: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    is_current: bool
    location: Optional[str]
    technologies: Optional[List[str]]
    achievements: Optional[List[str]]

    model_config = ConfigDict(from_attributes=True)


class CandidateEducationResponse(BaseModel):
    id: str
    institution_name: str
    degree: str
    field_of_study: Optional[str]
    start_date: Optional[date]
    end_date: Optional[date]
    is_current: bool
    grade: Optional[str]
    description: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class CandidateProjectResponse(BaseModel):
    id: str
    name: str
    description: Optional[str]
    technologies: Optional[List[str]]
    start_date: Optional[date]
    end_date: Optional[date]
    url: Optional[str]
    repository_url: Optional[str]
    is_featured: bool

    model_config = ConfigDict(from_attributes=True)


class CandidateProfileMetrics(BaseModel):
    interviews_count: int
    applications_count: int
    resume_count: int
    profile_completion_percentage: int
    last_activity: Optional[str]


class CandidateDetailedResponse(BaseModel):
    # Basic candidate info
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

    # Related data
    experiences: List[CandidateExperienceResponse]
    education: List[CandidateEducationResponse]
    projects: List[CandidateProjectResponse]

    # Metrics and summary
    metrics: CandidateProfileMetrics

    model_config = ConfigDict(from_attributes=True)


class CandidateProfileSummary(BaseModel):
    """Summary view for candidate profile cards"""
    id: str
    name: str
    email: str
    status: CandidateStatusEnum
    job_category: Optional[JobCategoryEnum]
    city: Optional[str]
    country: Optional[str]
    profile_completion_percentage: int
    total_experience_years: int
    total_projects: int
    last_activity: Optional[str]
    created_at: Optional[datetime]

    model_config = ConfigDict(from_attributes=True)
