"""
Company Page Response Schemas - Response schemas for company pages
"""
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


# Note: Response schemas use plain strings, not domain enums


class CompanyPageResponse(BaseModel):
    """Response for a company page"""

    id: str = Field(..., description="Unique page ID")
    company_id: str = Field(..., description="Company ID")
    page_type: str = Field(..., description="Page type")
    title: str = Field(..., description="Page title")
    html_content: str = Field(..., description="Page HTML content")
    plain_text: str = Field(..., description="Plain text extracted from HTML")
    word_count: int = Field(..., description="Number of words in content")
    meta_description: Optional[str] = Field(None, description="Meta description for SEO")
    meta_keywords: List[str] = Field(..., description="SEO keywords")
    language: str = Field(..., description="Page language")
    status: str = Field(..., description="Page status")
    is_default: bool = Field(..., description="Whether this is the default page for this type")
    version: int = Field(..., description="Page version")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")
    published_at: Optional[datetime] = Field(None, description="Publication date")

    class Config:
        from_attributes = True


class CompanyPageListResponse(BaseModel):
    """Response for company page list"""

    pages: List[CompanyPageResponse] = Field(..., description="List of pages")
    total: int = Field(..., description="Total number of pages")

    class Config:
        from_attributes = True


class CompanyPageSummaryResponse(BaseModel):
    """Summary response for a company page (for lists)"""

    id: str = Field(..., description="Unique page ID")
    page_type: str = Field(..., description="Page type")
    title: str = Field(..., description="Page title")
    status: str = Field(..., description="Page status")
    is_default: bool = Field(..., description="Whether this is the default page for this type")
    version: int = Field(..., description="Page version")
    created_at: datetime = Field(..., description="Creation date")
    updated_at: datetime = Field(..., description="Last update date")
    published_at: Optional[datetime] = Field(None, description="Publication date")

    class Config:
        from_attributes = True
