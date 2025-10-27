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
        # Convert requirements dict to string if present
        requirements_str = None
        if dto.requirements:
            # Join requirements into a readable string
            requirements_str = "\n".join([f"{k}: {v}" for k, v in dto.requirements.items()])

        return cls(
            id=dto.id.value,
            title=dto.title,
            description=dto.description,
            requirements=requirements_str,
            responsibilities=None,  # Not available in current DTO
            location=dto.location,
            is_remote=(dto.work_location_type.value == "REMOTE") if dto.work_location_type else False,
            salary_range_min=dto.salary_range.min_salary if dto.salary_range else None,
            salary_range_max=dto.salary_range.max_salary if dto.salary_range else None,
            employment_type=dto.employment_type.value if dto.employment_type else None,
            experience_level=dto.position_level.value if dto.position_level else None,
            department=dto.department,
            public_slug=dto.public_slug,
            created_at=dto.created_at if dto.created_at else datetime.now(),
            company_id=dto.company_id.value
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
