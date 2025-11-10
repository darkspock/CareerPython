"""
Public Position Schemas
Phase 10: Response schemas for public job positions - simplified
"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from datetime import datetime, date

from adapters.http.admin.schemas.job_position import JobPositionPublicResponse


class PublicPositionResponse(BaseModel):
    """Response schema for public job position - only visible fields for candidates"""
    id: str
    title: str
    description: Optional[str] = None
    job_category: str
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None  # Changed to date to match JobPositionPublicResponse
    public_slug: Optional[str] = None
    # Only visible custom fields (filtered by workflow/stage configuration)
    visible_fields: Dict[str, Any] = {}
    created_at: datetime
    company_id: str

    class Config:
        from_attributes = True

    @classmethod
    def from_public_response(cls, public_response: JobPositionPublicResponse) -> "PublicPositionResponse":
        """Convert JobPositionPublicResponse to PublicPositionResponse"""
        return cls(
            id=public_response.id,
            title=public_response.title,
            description=public_response.description,
            job_category=public_response.job_category,
            open_at=public_response.open_at,
            application_deadline=public_response.application_deadline,
            public_slug=public_response.public_slug,
            visible_fields=public_response.visible_fields,
            created_at=public_response.created_at if public_response.created_at else datetime.now(),
            company_id=public_response.company_id
        )


class PublicPositionListResponse(BaseModel):
    """Response schema for list of public positions with pagination"""
    positions: List[PublicPositionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class SubmitApplicationRequest(BaseModel):
    """Request schema for submitting an application"""
    cover_letter: Optional[str] = None
    referral_source: Optional[str] = None


class SubmitApplicationResponse(BaseModel):
    """Response schema after submitting an application"""
    application_id: str
    message: str
