"""Job position admin schemas - simplified version"""
from datetime import datetime, date
from typing import Optional, List, Dict, Any, Union

from pydantic import BaseModel, Field, field_validator

from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto


class JobPositionCreate(BaseModel):
    """Schema for creating a job position - simplified"""
    company_id: str = Field(..., description="Company ID")
    job_position_workflow_id: Optional[str] = Field(None, description="Workflow ID")
    stage_id: Optional[str] = Field(None, description="Initial stage ID")
    phase_workflows: Optional[Dict[str, str]] = Field(None, description="Phase workflows mapping")
    custom_fields_values: Optional[Dict[str, Any]] = Field(default_factory=dict,
                                                           description="Custom field values (all removed fields go here)")
    title: str = Field(..., description="Position title")
    description: Optional[str] = Field(None, description="Position description")
    job_category: Optional[str] = Field("other", description="Job category")
    open_at: Optional[datetime] = Field(None, description="When position opens")
    application_deadline: Optional[date] = Field(None, description="Application deadline")
    visibility: str = Field("hidden", description="Visibility level: hidden, internal, or public")
    public_slug: Optional[str] = Field(None, description="Public URL slug")

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
    """Schema for updating a job position - simplified"""
    job_position_workflow_id: Optional[str] = Field(None, description="Workflow ID")
    stage_id: Optional[str] = Field(None, description="Stage ID")
    phase_workflows: Optional[Dict[str, str]] = Field(None, description="Phase workflows mapping")
    custom_fields_values: Optional[Dict[str, Any]] = Field(None,
                                                           description="Custom field values (all removed fields go here)")
    title: Optional[str] = Field(None, description="Position title")
    description: Optional[str] = Field(None, description="Position description")
    job_category: Optional[str] = Field(None, description="Job category")
    open_at: Optional[datetime] = Field(None, description="When position opens")
    application_deadline: Optional[date] = Field(None, description="Application deadline")
    visibility: Optional[str] = Field(None, description="Visibility level: hidden, internal, or public")
    public_slug: Optional[str] = Field(None, description="Public URL slug")

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
    """Schema for job position response - simplified"""
    id: str
    title: str
    company_id: str
    job_position_workflow_id: Optional[str] = None  # Workflow system
    stage_id: Optional[str] = None  # Current stage
    phase_workflows: Optional[Dict[str, str]] = None  # Phase workflows mapping
    custom_fields_values: Dict[str, Any] = Field(
        default_factory=dict)  # Custom field values (contains all removed fields)
    company_name: Optional[str] = None  # For display purposes
    description: Optional[str] = None
    job_category: str = "other"
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    visibility: str  # JobPositionVisibilityEnum value
    public_slug: Optional[str] = None
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    pending_comments_count: int = 0  # Number of pending comments

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
            pending_comments_count=dto.pending_comments_count
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
