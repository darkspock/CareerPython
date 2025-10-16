from __future__ import annotations

from datetime import date, datetime
from typing import Optional, List, Dict, Any

from pydantic import BaseModel, field_validator, ConfigDict

from src.candidate.domain.enums import CandidateTypeEnum
from src.candidate.domain.enums.candidate_enums import WorkModalityEnum, LanguageLevelEnum, LanguageEnum, CandidateStatusEnum, PositionRoleEnum
from src.shared.domain.enums.job_category import JobCategoryEnum


class CandidateStatusUpdate(BaseModel):
    status: CandidateStatusEnum


class CandidateCreate(BaseModel):
    name: str
    date_of_birth: str
    city: str
    country: str
    phone: str
    email: str
    job_category: JobCategoryEnum
    expected_annual_salary: Optional[int] = None
    currency: Optional[str] = None
    relocation: Optional[bool] = None
    work_modality: List[WorkModalityEnum] = []
    languages: Dict[LanguageEnum, LanguageLevelEnum] = {}
    type: CandidateTypeEnum = CandidateTypeEnum.BASIC

    @field_validator('job_category', mode='before')
    @classmethod
    def validate_job_category(cls, v: Any) -> JobCategoryEnum:
        if isinstance(v, JobCategoryEnum):
            return v
        if isinstance(v, str):
            # Try to find enum by value first (e.g., "Technology" -> JobCategoryEnum.TECHNOLOGY)
            for enum_item in JobCategoryEnum:
                if enum_item.value == v:
                    return enum_item
            # If not found by value, try by name (e.g., "TECHNOLOGY" -> JobCategoryEnum.TECHNOLOGY)
            try:
                return JobCategoryEnum[v.upper()]
            except KeyError:
                pass
        raise ValueError(f"Invalid job category: {v}")

    model_config = ConfigDict(from_attributes=True)


class CandidateUpdate(BaseModel):
    job_category: JobCategoryEnum
    name: str
    phone: str
    email: str
    city: str
    country: str
    date_of_birth: str
    linkedin_url: Optional[str] = None
    # status is managed internally, not user-editable
    expected_annual_salary: Optional[int] = None
    current_annual_salary: Optional[int] = None
    currency: Optional[str] = None
    relocation: Optional[bool] = None
    work_modality: Optional[List[WorkModalityEnum]] = None
    languages: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None
    skills: Optional[List[str]] = None
    current_roles: Optional[List[PositionRoleEnum]] = None
    expected_roles: Optional[List[PositionRoleEnum]] = None
    type: Optional[CandidateTypeEnum] = None

    @field_validator('job_category', mode='before')
    @classmethod
    def validate_job_category(cls, v: Any) -> JobCategoryEnum:
        if isinstance(v, JobCategoryEnum):
            return v
        if isinstance(v, str):
            # Try to find enum by value first (e.g., "Technology" -> JobCategoryEnum.TECHNOLOGY)
            for enum_item in JobCategoryEnum:
                if enum_item.value == v:
                    return enum_item
            # If not found by value, try by name (e.g., "TECHNOLOGY" -> JobCategoryEnum.TECHNOLOGY)
            try:
                return JobCategoryEnum[v.upper()]
            except KeyError:
                pass
        raise ValueError(f"Invalid job category: {v}")

    model_config = ConfigDict(from_attributes=True)


class CandidateResponse(BaseModel):
    id: str
    name: str
    date_of_birth: str
    city: str
    country: str
    phone: str
    email: str
    user_id: str
    status: str
    job_category: str
    linkedin_url: Optional[str] = None
    expected_annual_salary: Optional[int] = None
    current_annual_salary: Optional[int] = None
    currency: Optional[str] = None
    relocation: Optional[bool] = None
    work_modality: Optional[List[str]] = None
    languages: Optional[Dict[str, str]] = None
    skills: Optional[List[str]] = None
    current_roles: Optional[List[str]] = None
    expected_roles: Optional[List[str]] = None
    type: str = CandidateTypeEnum.BASIC.value
    created_at: Optional[str] = None
    updated_at: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

    @field_validator('id', mode='before')
    @classmethod
    def format_id(cls, v: Any) -> str:
        if hasattr(v, 'value'):
            return str(v.value)
        return str(v)

    @field_validator('user_id', mode='before')
    @classmethod
    def format_user_id(cls, v: Any) -> str:
        if hasattr(v, 'value'):
            return str(v.value)
        return str(v)

    @field_validator('date_of_birth', mode='before')
    @classmethod
    def format_date_of_birth(cls, v: Any) -> str:
        if isinstance(v, date):
            return v.isoformat()
        return str(v)

    @field_validator('created_at', 'updated_at', mode='before')
    @classmethod
    def format_dates(cls, v: Any) -> Optional[str]:
        if v is None:
            return None
        if isinstance(v, (date, datetime)):
            return v.isoformat()
        return str(v)


class CandidateListResponse(BaseModel):
    items: List[CandidateResponse]


CandidateResponse.model_rebuild()
