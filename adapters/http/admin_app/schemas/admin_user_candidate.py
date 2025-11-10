from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List, Dict
from datetime import datetime

from src.candidate_bc.candidate.domain.enums import WorkModalityEnum, LanguageLevelEnum, CandidateTypeEnum, CandidateStatusEnum
from src.framework.domain.enums.job_category import JobCategoryEnum


class AdminUserCandidateCreate(BaseModel):
    """Schema for admin to create a new user and candidate in one operation"""

    # User data
    email: EmailStr = Field(..., description="User's email address")
    password: str = Field(..., min_length=8, description="User's password (will be hashed)")

    # Candidate data
    name: str = Field(..., description="Candidate's full name")
    date_of_birth: str = Field(..., description="Date of birth in YYYY-MM-DD format")
    city: str = Field(..., description="City where candidate lives")
    country: str = Field(..., description="Country where candidate lives")
    phone: str = Field(..., description="Phone number")
    job_category: JobCategoryEnum = Field(..., description="Primary job category")
    expected_annual_salary: Optional[int] = Field(None, description="Expected annual salary")
    currency: Optional[str] = Field("USD", description="Currency for salary")
    relocation: Optional[bool] = Field(False, description="Willing to relocate")
    work_modality: List[WorkModalityEnum] = Field(default_factory=list, description="Preferred work modalities")
    languages: Dict[LanguageLevelEnum, LanguageLevelEnum] = Field(default_factory=dict, description="Languages and proficiency levels")
    type: CandidateTypeEnum = Field(CandidateTypeEnum.BASIC, description="Candidate type")

    # Admin fields
    initial_status: CandidateStatusEnum = Field(CandidateStatusEnum.DRAFT, description="Initial candidate status")
    admin_notes: Optional[str] = Field(None, description="Admin notes about the user/candidate")

    class Config:
        from_attributes = True


class AdminUserCandidateResponse(BaseModel):
    """Response schema for created user and candidate"""

    # User data
    user_id: str
    email: str
    user_created_at: datetime

    # Candidate data
    candidate_id: str
    name: str
    date_of_birth: str
    city: str
    country: str
    phone: str
    status: CandidateStatusEnum
    job_category: JobCategoryEnum
    expected_annual_salary: Optional[int]
    currency: Optional[str]
    relocation: Optional[bool]
    work_modality: List[WorkModalityEnum]
    languages: Dict[LanguageLevelEnum, LanguageLevelEnum]
    type: CandidateTypeEnum
    candidate_created_at: datetime

    # Admin metadata
    created_by_admin: str
    admin_notes: Optional[str]

    class Config:
        from_attributes = True


class AdminUserUpdate(BaseModel):
    """Schema for admin to update user information"""
    email: Optional[EmailStr] = None
    new_password: Optional[str] = Field(None, min_length=8, description="New password (will be hashed)")
    is_active: Optional[bool] = None
    admin_notes: Optional[str] = None

    class Config:
        from_attributes = True


class AdminUserResponse(BaseModel):
    """Response schema for user information in admin context"""
    id: str
    email: str
    is_active: bool
    created_at: datetime
    updated_at: Optional[datetime]
    last_login: Optional[datetime]

    # Related candidate info (if exists)
    has_candidate_profile: bool
    candidate_id: Optional[str]
    candidate_name: Optional[str]
    candidate_status: Optional[CandidateStatusEnum]

    class Config:
        from_attributes = True
