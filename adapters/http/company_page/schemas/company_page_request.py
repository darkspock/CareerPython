"""
Company Page Request Schemas - Request schemas for company pages
"""
from typing import List, Optional
from pydantic import BaseModel, Field, validator

from src.company_bc.company_page.domain.enums.page_type import PageType


class CreateCompanyPageRequest(BaseModel):
    """Request to create a company page"""
    
    page_type: PageType = Field(..., description="Page type")
    title: str = Field(..., min_length=1, max_length=500, description="Page title")
    html_content: str = Field(..., min_length=1, description="Page HTML content")
    meta_description: Optional[str] = Field(None, max_length=160, description="Meta description for SEO")
    meta_keywords: List[str] = Field(default_factory=list, max_length=20, description="SEO keywords")
    language: str = Field(default="en", min_length=2, max_length=2, description="Page language")
    is_default: bool = Field(default=False, description="Whether this is the default page for this type")
    
    @validator('meta_keywords')
    def validate_keywords(cls, v: List[str]) -> List[str]:
        if len(v) > 20:
            raise ValueError('Maximum 20 keywords allowed')
        if any(not keyword.strip() for keyword in v):
            raise ValueError('Keywords cannot be empty')
        return v
    
    @validator('language')
    def validate_language(cls, v: str) -> str:
        if len(v) != 2:
            raise ValueError('Language must be a 2-character code')
        return v.lower()


class UpdateCompanyPageRequest(BaseModel):
    """Request to update a company page"""
    
    title: str = Field(..., min_length=1, max_length=500, description="Page title")
    html_content: str = Field(..., min_length=1, description="Page HTML content")
    meta_description: Optional[str] = Field(None, max_length=160, description="Meta description for SEO")
    meta_keywords: List[str] = Field(default_factory=list, max_length=20, description="SEO keywords")
    
    @validator('meta_keywords')
    def validate_keywords(cls, v: List[str]) -> List[str]:
        if len(v) > 20:
            raise ValueError('Maximum 20 keywords allowed')
        if any(not keyword.strip() for keyword in v):
            raise ValueError('Keywords cannot be empty')
        return v
