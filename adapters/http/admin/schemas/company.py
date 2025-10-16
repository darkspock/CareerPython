"""Company admin schemas"""
from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, Field, field_validator


class CompanyBase(BaseModel):
    """Base company schema"""
    name: str = Field(..., min_length=1, max_length=200, description="Company name")
    sector: Optional[str] = Field(None, max_length=100, description="Company sector/industry")
    size: Optional[int] = Field(None, ge=1, description="Number of employees")
    location: Optional[str] = Field(None, max_length=200, description="Company location")
    website: Optional[str] = Field(None, max_length=500, description="Company website URL")
    culture: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Company culture information")
    external_data: Optional[Dict[str, Any]] = Field(default_factory=dict, description="External data")

    @field_validator('website')
    @classmethod
    def validate_website(cls, v: Optional[str]) -> Optional[str]:
        """Simply return the website as-is without validation"""
        if not v:
            return v
        # Just return the value as-is, no validation
        return v.strip() if v else v


class CompanyCreate(CompanyBase):
    """Schema for creating a company"""
    user_id: Optional[str] = Field(None, description="User ID who owns the company (optional)")


class CompanyUpdate(BaseModel):
    """Schema for updating a company"""
    name: Optional[str] = Field(None, min_length=1, max_length=200, description="Company name")
    sector: Optional[str] = Field(None, max_length=255)
    size: Optional[int] = Field(None, ge=1)
    location: Optional[str] = Field(None, max_length=255)
    website: Optional[str] = Field(None, max_length=500)
    culture: Optional[Dict[str, Any]] = None
    external_data: Optional[Dict[str, Any]] = None


class CompanyResponse(CompanyBase):
    """Schema for company response"""
    id: str = Field(..., description="Company ID")
    user_id: Optional[str] = Field(None, description="User ID who owns the company (optional)")
    status: str = Field(..., description="Company approval status")
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
