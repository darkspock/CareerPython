"""Job position admin schemas - simplified version"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union

from pydantic import BaseModel, Field, field_validator

from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto


class JobPositionCreate(BaseModel):
    """Schema for creating a job position"""
    company_id: str = Field(..., description="Company ID")
    job_position_workflow_id: Optional[str] = Field(None, description="Workflow ID")
    stage_id: Optional[str] = Field(None, description="Initial stage ID")
    phase_workflows: Optional[Dict[str, str]] = Field(None, description="Phase workflows mapping")
    custom_fields_values: Optional[Dict[str, Any]] = Field(default_factory=dict,
                                                           description="Custom field values")
    title: str = Field(..., description="Position title")
    description: Optional[str] = Field(None, description="Position description")
    job_category: Optional[str] = Field("other", description="Job category")
    open_at: Optional[datetime] = Field(None, description="When position opens")
    application_deadline: Optional[date] = Field(None, description="Application deadline")
    visibility: str = Field("hidden", description="Visibility level: hidden, internal, or public")
    public_slug: Optional[str] = Field(None, description="Public URL slug")
    # New publishing flow fields
    screening_template_id: Optional[str] = Field(None, description="Screening interview template ID")
    skills: Optional[List[str]] = Field(None, description="Required skills")
    department_id: Optional[str] = Field(None, description="Department ID")
    employment_type: Optional[str] = Field(None, description="Employment type")
    experience_level: Optional[str] = Field(None, description="Experience level required")
    work_location_type: Optional[str] = Field(None, description="Work location type")
    office_locations: Optional[List[str]] = Field(None, description="Office locations")
    remote_restrictions: Optional[str] = Field(None, description="Remote work restrictions")
    number_of_openings: Optional[int] = Field(1, description="Number of openings")
    requisition_id: Optional[str] = Field(None, description="Internal requisition ID")
    salary_currency: Optional[str] = Field(None, description="Salary currency code")
    salary_min: Optional[float] = Field(None, description="Minimum salary")
    salary_max: Optional[float] = Field(None, description="Maximum salary")
    salary_period: Optional[str] = Field(None, description="Salary period: hourly, monthly, yearly")
    show_salary: Optional[bool] = Field(False, description="Show salary to candidates")
    budget_max: Optional[float] = Field(None, description="Maximum budget for this position")
    hiring_manager_id: Optional[str] = Field(None, description="Hiring manager user ID")
    recruiter_id: Optional[str] = Field(None, description="Recruiter user ID")

    @field_validator('application_deadline', mode='before')
    @classmethod
    def validate_application_deadline(cls, v: Union[str, date, None]) -> Optional[date]:
        """Convert empty strings to None for optional date field"""
        if v is None:
            return None
        if isinstance(v, str):
            if not v.strip():
                return None
            # Let Pydantic parse the string to date
            return v  # type: ignore[return-value]
        # If it's already a date object, return it
        return v

    @field_validator('visibility', mode='before')
    @classmethod
    def validate_visibility(cls, v: Union[str, None]) -> str:
        """Normalize visibility to lowercase"""
        if v is None:
            return "hidden"
        # Convert to lowercase to match enum values
        return v.lower()

    class Config:
        use_enum_values = True


class JobPositionUpdate(BaseModel):
    """Schema for updating a job position"""
    job_position_workflow_id: Optional[str] = Field(None, description="Workflow ID")
    stage_id: Optional[str] = Field(None, description="Stage ID")
    phase_workflows: Optional[Dict[str, str]] = Field(None, description="Phase workflows mapping")
    custom_fields_values: Optional[Dict[str, Any]] = Field(None, description="Custom field values")
    title: Optional[str] = Field(None, description="Position title")
    description: Optional[str] = Field(None, description="Position description")
    job_category: Optional[str] = Field(None, description="Job category")
    open_at: Optional[datetime] = Field(None, description="When position opens")
    application_deadline: Optional[date] = Field(None, description="Application deadline")
    visibility: Optional[str] = Field(None, description="Visibility level: hidden, internal, or public")
    public_slug: Optional[str] = Field(None, description="Public URL slug")
    # New publishing flow fields
    screening_template_id: Optional[str] = Field(None, description="Screening interview template ID")
    skills: Optional[List[str]] = Field(None, description="Required skills")
    department_id: Optional[str] = Field(None, description="Department ID")
    employment_type: Optional[str] = Field(None, description="Employment type")
    experience_level: Optional[str] = Field(None, description="Experience level required")
    work_location_type: Optional[str] = Field(None, description="Work location type")
    office_locations: Optional[List[str]] = Field(None, description="Office locations")
    remote_restrictions: Optional[str] = Field(None, description="Remote work restrictions")
    number_of_openings: Optional[int] = Field(None, description="Number of openings")
    requisition_id: Optional[str] = Field(None, description="Internal requisition ID")
    salary_currency: Optional[str] = Field(None, description="Salary currency code")
    salary_min: Optional[float] = Field(None, description="Minimum salary")
    salary_max: Optional[float] = Field(None, description="Maximum salary")
    salary_period: Optional[str] = Field(None, description="Salary period: hourly, monthly, yearly")
    show_salary: Optional[bool] = Field(None, description="Show salary to candidates")
    budget_max: Optional[float] = Field(None, description="Maximum budget for this position")
    hiring_manager_id: Optional[str] = Field(None, description="Hiring manager user ID")
    recruiter_id: Optional[str] = Field(None, description="Recruiter user ID")

    @field_validator('visibility', mode='before')
    @classmethod
    def validate_visibility(cls, v: Union[str, None]) -> Optional[str]:
        """Normalize visibility to lowercase"""
        if v is None:
            return None
        # Convert to lowercase to match enum values
        return v.lower()

    @field_validator('application_deadline', mode='before')
    @classmethod
    def validate_application_deadline(cls, v: Union[str, date, None]) -> Optional[date]:
        """Convert empty strings to None for optional date field"""
        if v is None:
            return None
        if isinstance(v, str):
            if not v.strip():
                return None
            # Let Pydantic parse the string to date
            return v  # type: ignore[return-value]
        # If it's already a date object, return it
        return v

    class Config:
        use_enum_values = True


class JobPositionResponse(BaseModel):
    """Schema for job position response"""
    id: str
    title: str
    company_id: str
    job_position_workflow_id: Optional[str] = None
    stage_id: Optional[str] = None
    phase_workflows: Optional[Dict[str, str]] = None
    custom_fields_values: Dict[str, Any] = Field(default_factory=dict)
    company_name: Optional[str] = None
    description: Optional[str] = None
    job_category: str = "other"
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    visibility: str
    public_slug: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pending_comments_count: int = 0
    # Publishing flow fields
    status: Optional[str] = None
    screening_template_id: Optional[str] = None
    skills: Optional[List[str]] = None
    department_id: Optional[str] = None
    employment_type: Optional[str] = None
    experience_level: Optional[str] = None
    work_location_type: Optional[str] = None
    office_locations: Optional[List[str]] = None
    remote_restrictions: Optional[str] = None
    number_of_openings: Optional[int] = None
    requisition_id: Optional[str] = None
    salary_currency: Optional[str] = None
    salary_min: Optional[float] = None
    salary_max: Optional[float] = None
    salary_period: Optional[str] = None
    show_salary: Optional[bool] = None
    budget_max: Optional[float] = None
    hiring_manager_id: Optional[str] = None
    recruiter_id: Optional[str] = None
    closed_reason: Optional[str] = None
    closed_at: Optional[datetime] = None
    published_at: Optional[datetime] = None

    class Config:
        use_enum_values = True

    @classmethod
    def from_dto(cls, dto: JobPositionDto, company_name: Optional[str] = None) -> 'JobPositionResponse':
        """Convert JobPositionDto to JobPositionResponse"""
        return cls(
            id=dto.id.value,
            title=dto.title,
            company_id=dto.company_id.value,
            job_position_workflow_id=dto.job_position_workflow_id,
            stage_id=dto.stage_id,
            phase_workflows=dto.phase_workflows,
            custom_fields_values=dto.custom_fields_values,
            company_name=company_name,
            description=dto.description,
            job_category=dto.job_category.value,
            open_at=dto.open_at,
            application_deadline=dto.application_deadline,
            visibility=dto.visibility,
            public_slug=dto.public_slug,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            pending_comments_count=dto.pending_comments_count,
            status=dto.status,
            screening_template_id=dto.screening_template_id,
            skills=dto.skills,
            department_id=dto.department_id,
            employment_type=dto.employment_type,
            experience_level=dto.experience_level,
            work_location_type=dto.work_location_type,
            office_locations=dto.office_locations,
            remote_restrictions=dto.remote_restrictions,
            number_of_openings=dto.number_of_openings,
            requisition_id=dto.requisition_id,
            salary_currency=dto.salary_currency,
            salary_min=float(dto.salary_min) if dto.salary_min else None,
            salary_max=float(dto.salary_max) if dto.salary_max else None,
            salary_period=dto.salary_period,
            show_salary=dto.show_salary,
            budget_max=float(dto.budget_max) if dto.budget_max else None,
            hiring_manager_id=dto.hiring_manager_id,
            recruiter_id=dto.recruiter_id,
            closed_reason=dto.closed_reason,
            closed_at=dto.closed_at,
            published_at=dto.published_at
        )


class JobPositionPublicResponse(BaseModel):
    """Schema for public job position response - only visible fields for candidates"""
    id: str
    title: str
    company_id: str
    description: Optional[str] = None
    job_category: str
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    public_slug: Optional[str] = None
    # Only visible custom fields (filtered by workflow/stage configuration)
    visible_fields: Dict[str, Any] = Field(default_factory=dict)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True


class JobPositionListResponse(BaseModel):
    """Schema for job position list response"""
    positions: List[JobPositionResponse]
    total: int
    page: int
    page_size: int
    total_pages: int


class JobPositionStatsResponse(BaseModel):
    """Schema for job position statistics response"""
    total_positions: int
    active_positions: int
    inactive_positions: int
    positions_by_type: Dict[str, int] = Field(default_factory=dict)
    positions_by_company: Dict[str, int] = Field(default_factory=dict)


class JobPositionActionResponse(BaseModel):
    """Schema for job position action response"""
    success: bool
    message: str
    position_id: Optional[str] = None


# ==================== STATUS TRANSITION REQUEST SCHEMAS ====================

class RejectJobPositionRequest(BaseModel):
    """Request schema for rejecting a job position"""
    reason: Optional[str] = Field(None, description="Reason for rejection")


class CloseJobPositionRequest(BaseModel):
    """Request schema for closing a job position"""
    reason: str = Field(..., description="Close reason: filled, cancelled, budget_cut, duplicate, other")
    note: Optional[str] = Field(None, description="Optional note about the closure")


class CreateInlineScreeningTemplateRequest(BaseModel):
    """Request schema for creating inline screening template"""
    name: Optional[str] = Field(None, description="Template name (defaults to position title)")
    intro: Optional[str] = Field(None, description="Introduction text for the screening")
    prompt: Optional[str] = Field(None, description="Prompt for the interviewer")
    goal: Optional[str] = Field(None, description="Goal of the screening")


class CreateInlineScreeningTemplateResponse(BaseModel):
    """Response schema for inline screening template creation"""
    success: bool
    message: str
    template_id: Optional[str] = None
    position_id: Optional[str] = None
