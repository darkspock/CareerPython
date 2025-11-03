"""Job position admin schemas"""
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from datetime import datetime, date

from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.job_position.domain.enums import JobPositionStatusEnum, ContractTypeEnum, WorkLocationTypeEnum
from src.job_position.domain.enums.employment_type import EmploymentType
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.shared.domain.enums.job_category import JobCategoryEnum
from src.job_position.application.queries.job_position_dto import JobPositionDto


class JobPositionCreate(BaseModel):
    """Schema for creating a job position"""
    company_id: str = Field(..., description="Company ID")
    workflow_id: Optional[str] = Field(None, description="Workflow ID")
    title: str = Field(..., description="Position title")
    description: Optional[str] = Field(None, description="Position description")
    location: Optional[str] = Field(None, description="Position location")
    department: Optional[str] = Field(None, description="Department")
    employment_type: str = Field("full_time", description="Employment type")
    experience_level: str = Field("mid", description="Experience level")
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")
    salary_currency: Optional[str] = Field("USD", description="Salary currency")
    requirements: Optional[List[str]] = Field(default_factory=list, description="Requirements")
    benefits: Optional[List[str]] = Field(default_factory=list, description="Benefits")
    skills: Optional[List[str]] = Field(default_factory=list, description="Required skills")
    is_remote: bool = Field(False, description="Remote work available")
    application_deadline: Optional[str] = Field(None, description="Application deadline")
    application_url: Optional[str] = Field(None, description="Application URL")
    application_email: Optional[str] = Field(None, description="Application email")
    # Additional fields
    working_hours: Optional[str] = Field(None, description="Working hours")
    travel_required: Optional[bool] = Field(False, description="Whether travel is required")
    visa_sponsorship: Optional[bool] = Field(False, description="Visa sponsorship available")
    contact_person: Optional[str] = Field(None, description="Contact person")
    reports_to: Optional[str] = Field(None, description="Reports to")
    number_of_openings: Optional[int] = Field(1, description="Number of openings")
    job_category: Optional[str] = Field("other", description="Job category")
    languages_required: Optional[Dict[str, str]] = Field(None, description="Languages required")
    desired_roles: Optional[List[str]] = Field(None, description="Desired roles")


class JobPositionUpdate(BaseModel):
    """Schema for updating a job position"""
    workflow_id: Optional[str] = Field(None, description="Workflow ID")
    title: Optional[str] = Field(None, description="Position title")
    description: Optional[str] = Field(None, description="Position description")
    location: Optional[str] = Field(None, description="Position location")
    department: Optional[str] = Field(None, description="Department")
    employment_type: Optional[str] = Field(None, description="Employment type")
    experience_level: Optional[str] = Field(None, description="Experience level")
    salary_min: Optional[int] = Field(None, description="Minimum salary")
    salary_max: Optional[int] = Field(None, description="Maximum salary")
    salary_currency: Optional[str] = Field(None, description="Salary currency")
    requirements: Optional[List[str]] = Field(None, description="Requirements")
    benefits: Optional[List[str]] = Field(None, description="Benefits")
    skills: Optional[List[str]] = Field(None, description="Required skills")
    is_remote: Optional[bool] = Field(None, description="Remote work available")
    application_deadline: Optional[str] = Field(None, description="Application deadline")
    application_url: Optional[str] = Field(None, description="Application URL")
    application_email: Optional[str] = Field(None, description="Application email")
    # Additional fields for completeness
    working_hours: Optional[str] = Field(None, description="Working hours")
    travel_required: Optional[bool] = Field(False, description="Whether travel is required")
    visa_sponsorship: Optional[bool] = Field(None, description="Visa sponsorship available")
    contact_person: Optional[str] = Field(None, description="Contact person")
    reports_to: Optional[str] = Field(None, description="Reports to")
    number_of_openings: Optional[int] = Field(None, description="Number of openings")
    job_category: Optional[str] = Field(None, description="Job category")
    languages_required: Optional[Dict[str, str]] = Field(None, description="Languages required")
    desired_roles: Optional[List[str]] = Field(None, description="Desired roles")


class JobPositionResponse(BaseModel):
    """Schema for job position response"""
    id: str
    title: str
    company_id: str
    workflow_id: Optional[str] = None
    company_name: Optional[str] = None  # For display purposes
    description: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    work_location_type: WorkLocationTypeEnum = WorkLocationTypeEnum.ON_SITE
    salary_range: Optional[Dict[str, Any]] = None  # Serialized SalaryRange
    contract_type: ContractTypeEnum = ContractTypeEnum.FULL_TIME
    requirements: Optional[Dict[str, Any]] = Field(default_factory=dict)
    job_category: JobCategoryEnum = JobCategoryEnum.OTHER
    position_level: Optional[JobPositionLevelEnum] = None
    number_of_openings: int = 1
    application_instructions: Optional[str] = None
    benefits: List[str] = Field(default_factory=list)
    working_hours: Optional[str] = None
    travel_required: Optional[int] = None  # percentage (0-100)
    languages_required: Dict[str, str] = Field(default_factory=dict)  # Serialized enum dict
    visa_sponsorship: bool = False
    contact_person: Optional[str] = None
    department: Optional[str] = None
    reports_to: Optional[str] = None
    status: JobPositionStatusEnum = JobPositionStatusEnum.PENDING
    desired_roles: Optional[List[str]] = None  # Serialized PositionRoleEnum list
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    application_url: Optional[str] = None
    application_email: Optional[str] = None
    skills: List[str] = Field(default_factory=list)
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        use_enum_values = True

    @classmethod
    def from_dto(cls, dto: JobPositionDto, company_name: Optional[str] = None) -> 'JobPositionResponse':
        """Convert JobPositionDto to JobPositionResponse"""
        # Serialize salary_range
        salary_range_dict = None
        if dto.salary_range:
            salary_range_dict = {
                "min_amount": dto.salary_range.min_salary,
                "max_amount": dto.salary_range.max_salary,
                "currency": dto.salary_range.currency
            }

        # Serialize languages_required
        languages_dict = {}
        if dto.languages_required:
            languages_dict = {
                lang.value: level.value
                for lang, level in dto.languages_required.items()
            }

        # Serialize desired_roles
        desired_roles_list = None
        if dto.desired_roles:
            desired_roles_list = [role.value for role in dto.desired_roles]

        return cls(
            id=dto.id.value,
            title=dto.title,
            company_id=dto.company_id.value,
            workflow_id=dto.workflow_id,
            company_name=company_name,
            description=dto.description,
            location=dto.location,
            employment_type=dto.employment_type,
            work_location_type=dto.work_location_type,
            salary_range=salary_range_dict,
            contract_type=dto.contract_type,
            requirements=dto.requirements,
            job_category=dto.job_category,
            position_level=dto.position_level,
            number_of_openings=dto.number_of_openings,
            application_instructions=dto.application_instructions,
            benefits=dto.benefits or [],
            working_hours=dto.working_hours,
            travel_required=dto.travel_required,
            languages_required=languages_dict,
            visa_sponsorship=dto.visa_sponsorship,
            contact_person=dto.contact_person,
            department=dto.department,
            reports_to=dto.reports_to,
            status=dto.status,
            desired_roles=desired_roles_list,
            open_at=dto.open_at,
            application_deadline=dto.application_deadline,
            application_url=dto.application_url,
            application_email=dto.application_email,
            skills=dto.skills or [],
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )


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
