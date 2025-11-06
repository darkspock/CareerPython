from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field, validator, ConfigDict

from src.company.domain.enums import CompanyStatusEnum


class CompanyBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    sector: Optional[str] = Field(None, max_length=255)
    size: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    culture: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None

    @validator('website')
    def validate_website(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v


class CompanyCreate(CompanyBase):
    user_id: str = Field(..., min_length=1)


class CompanyUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    sector: Optional[str] = Field(None, max_length=255)
    size: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    culture: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None

    @validator('website')
    def validate_website(cls, v: Optional[str]) -> Optional[str]:
        if v and not v.startswith(('http://', 'https://')):
            return f"https://{v}"
        return v


class CompanyApproval(BaseModel):
    approval_notes: Optional[str] = Field(None, max_length=1000)


class CompanyRejection(BaseModel):
    rejection_reason: str = Field(..., min_length=1, max_length=1000)


class CompanyDeactivation(BaseModel):
    deactivation_reason: str = Field(..., min_length=1, max_length=1000)


class CompanyResponse(BaseModel):
    id: str
    user_id: str
    name: str
    sector: Optional[str]
    size: Optional[int]
    location: Optional[str]
    website: Optional[str]
    culture: Optional[Dict[str, Any]]
    external_data: Optional[Dict[str, Any]]
    status: CompanyStatusEnum
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class CompanyListResponse(BaseModel):
    companies: list[CompanyResponse]
    total_count: int
    has_more: bool


class CompanyStatsResponse(BaseModel):
    total_count: int
    pending_count: int
    approved_count: int
    rejected_count: int
    active_count: int
    inactive_count: int
    recent_count: int
