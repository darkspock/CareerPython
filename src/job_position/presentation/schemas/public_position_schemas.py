"""
Public Position Schemas
Phase 10: Response schemas for public job positions
"""
from typing import Optional, List
from pydantic import BaseModel
from datetime import datetime

from src.job_position.application.queries.job_position_dto import JobPositionDto


class PublicPositionResponse(BaseModel):
    """Response schema for public job position"""
    id: str
    title: str
    description: Optional[str] = None
    requirements: Optional[str] = None
    responsibilities: Optional[str] = None
    location: Optional[str] = None
    is_remote: bool = False
    salary_range_min: Optional[float] = None
    salary_range_max: Optional[float] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    department: Optional[str] = None
    public_slug: Optional[str] = None
    created_at: datetime

    # Company info (if needed in future)
    company_id: str

    class Config:
        from_attributes = True

    @classmethod
    def from_dto(cls, dto: JobPositionDto) -> "PublicPositionResponse":
        """Convert DTO to response schema"""
        return cls(
            id=dto.id,
            title=dto.title,
            description=dto.description,
            requirements=dto.requirements,
            responsibilities=dto.responsibilities,
            location=dto.location,
            is_remote=dto.is_remote,
            salary_range_min=dto.salary_range_min,
            salary_range_max=dto.salary_range_max,
            employment_type=dto.contract_type.value if dto.contract_type else None,
            experience_level=dto.experience_level,
            department=dto.department,
            public_slug=dto.public_slug,
            created_at=dto.created_at,
            company_id=dto.company_id
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
