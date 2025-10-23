"""Company admin schemas"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator


class CompanyBase(BaseModel):
    """Base company schema"""
    name: str = Field(..., min_length=1, max_length=200, description="Company name")
    domain: str = Field(..., min_length=3, max_length=200, description="Company domain (e.g., company.com)")
    logo_url: Optional[str] = Field(None, max_length=500, description="Company logo URL")
    settings: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Company settings")

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: str) -> str:
        """Validate domain format"""
        if "@" in v:
            raise ValueError("Domain must not contain @")
        return v.strip().lower()


class CompanyCreate(CompanyBase):
    """Schema for creating a company"""
    pass


class CompanyUpdate(BaseModel):
    """Schema for updating a company"""
    name: str = Field(None, min_length=1, max_length=200, description="Company name")
    domain: Optional[str] = Field(None, min_length=3, max_length=200, description="Company domain")
    logo_url: Optional[str] = Field(None, max_length=500, description="Company logo URL")
    settings: Optional[Dict[str, Any]] = Field(None, description="Company settings")

    @field_validator('domain')
    @classmethod
    def validate_domain(cls, v: Optional[str]) -> Optional[str]:
        """Validate domain format"""
        if v and "@" in v:
            raise ValueError("Domain must not contain @")
        return v.strip().lower() if v else v


class CompanyResponse(CompanyBase):
    """Schema for company response"""
    id: str = Field(..., description="Company ID")
    status: str = Field(..., description="Company status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")

    class Config:
        from_attributes = True


class CompanyListResponse(BaseModel):
    """Schema for company list response"""
    companies: List[CompanyResponse] = Field(..., description="List of companies")
    total: int = Field(..., description="Total number of companies")
    page: int = Field(1, description="Current page number")
    page_size: int = Field(10, description="Number of items per page")
    total_pages: int = Field(..., description="Total number of pages")


class CompanyStatsResponse(BaseModel):
    """Schema for company statistics response"""
    total_companies: int = Field(..., description="Total number of companies")
    pending_approval: int = Field(..., description="Companies pending approval")
    approved_companies: int = Field(..., description="Approved companies")
    active_companies: int = Field(..., description="Active companies")
    rejected_companies: int = Field(..., description="Rejected companies")


class CompanyStatusUpdate(BaseModel):
    """Schema for updating company status"""
    reason: Optional[str] = Field(None, max_length=500, description="Reason for status change")


class CompanyActionResponse(BaseModel):
    """Schema for company action response"""
    message: str = Field(..., description="Action result message")
    affected_count: Optional[int] = Field(None, description="Number of affected companies")
    company: Optional[CompanyResponse] = Field(None, description="Updated company data")
