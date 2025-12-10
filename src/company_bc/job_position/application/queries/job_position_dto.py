"""Job position DTOs"""
from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, List, Dict, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.domain import JobPosition
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.language_requirement import LanguageRequirement
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPositionDto:
    """Full JobPosition DTO with all publishing flow fields"""
    # Core identification
    id: JobPositionId
    title: str
    company_id: CompanyId

    # Workflow system
    job_position_workflow_id: Optional[str]
    phase_workflows: Optional[Dict[str, str]]
    stage_id: Optional[str]

    # Content fields
    description: Optional[str]
    job_category: JobCategoryEnum
    skills: List[str]
    languages: List[Dict[str, str]]  # Serialized LanguageRequirement

    # Standard fields
    department_id: Optional[str]
    employment_type: Optional[str]
    experience_level: Optional[str]
    work_location_type: Optional[str]
    office_locations: List[str]
    remote_restrictions: Optional[str]
    number_of_openings: int
    requisition_id: Optional[str]

    # Financial fields
    salary_currency: Optional[str]
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    salary_period: Optional[str]
    show_salary: bool
    budget_max: Optional[Decimal]
    approved_budget_max: Optional[Decimal]
    financial_approver_id: Optional[str]
    approved_at: Optional[datetime]

    # Ownership fields
    hiring_manager_id: Optional[str]
    recruiter_id: Optional[str]
    created_by_id: Optional[str]

    # Lifecycle fields
    status: str
    closed_reason: Optional[str]
    closed_at: Optional[datetime]
    published_at: Optional[datetime]

    # Custom fields
    custom_fields_config: List[Dict[str, Any]]  # Serialized CustomFieldDefinition
    custom_fields_values: Dict[str, Any]
    source_workflow_id: Optional[str]

    # Pipeline and screening
    candidate_pipeline_id: Optional[str]
    screening_template_id: Optional[str]

    # Visibility and publishing
    visibility: str
    public_slug: Optional[str]
    open_at: Optional[datetime]
    application_deadline: Optional[date]

    # Timestamps
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    # Additional computed fields
    pending_comments_count: int = 0

    @staticmethod
    def from_entity(entity: JobPosition) -> 'JobPositionDto':
        """Create a JobPositionDto from a JobPosition entity"""
        # Convert languages to serializable format
        languages_data = LanguageRequirement.to_list(entity.languages) if entity.languages else []

        # Convert custom_fields_config to serializable format
        config_data = CustomFieldDefinition.to_list(entity.custom_fields_config) if entity.custom_fields_config else []

        return JobPositionDto(
            # Core identification
            id=entity.id,
            title=entity.title,
            company_id=entity.company_id,
            # Workflow system
            job_position_workflow_id=entity.job_position_workflow_id.value if entity.job_position_workflow_id else None,
            phase_workflows=entity.phase_workflows,
            stage_id=entity.stage_id.value if entity.stage_id else None,
            # Content fields
            description=entity.description,
            job_category=entity.job_category,
            skills=entity.skills or [],
            languages=languages_data,
            # Standard fields
            department_id=entity.department_id,
            employment_type=entity.employment_type.value if entity.employment_type else None,
            experience_level=entity.experience_level.value if entity.experience_level else None,
            work_location_type=entity.work_location_type.value if entity.work_location_type else None,
            office_locations=entity.office_locations or [],
            remote_restrictions=entity.remote_restrictions,
            number_of_openings=entity.number_of_openings,
            requisition_id=entity.requisition_id,
            # Financial fields
            salary_currency=entity.salary_currency,
            salary_min=entity.salary_min,
            salary_max=entity.salary_max,
            salary_period=entity.salary_period.value if entity.salary_period else None,
            show_salary=entity.show_salary,
            budget_max=entity.budget_max,
            approved_budget_max=entity.approved_budget_max,
            financial_approver_id=entity.financial_approver_id.value if entity.financial_approver_id else None,
            approved_at=entity.approved_at,
            # Ownership fields
            hiring_manager_id=entity.hiring_manager_id.value if entity.hiring_manager_id else None,
            recruiter_id=entity.recruiter_id.value if entity.recruiter_id else None,
            created_by_id=entity.created_by_id.value if entity.created_by_id else None,
            # Lifecycle fields
            status=entity.status.value if entity.status else "draft",
            closed_reason=entity.closed_reason.value if entity.closed_reason else None,
            closed_at=entity.closed_at,
            published_at=entity.published_at,
            # Custom fields
            custom_fields_config=config_data,
            custom_fields_values=entity.custom_fields_values or {},
            source_workflow_id=entity.source_workflow_id,
            # Pipeline and screening
            candidate_pipeline_id=entity.candidate_pipeline_id,
            screening_template_id=entity.screening_template_id,
            # Visibility and publishing
            visibility=entity.visibility.value,
            public_slug=entity.public_slug,
            open_at=entity.open_at,
            application_deadline=entity.application_deadline,
            # Timestamps
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )


@dataclass
class JobPositionPublicDto:
    """
    Public-facing JobPosition DTO for candidates.
    Excludes sensitive fields: budget_max, approved_budget_max, financial_approver_id,
    stage_assignments, created_by_id, and internal custom fields.
    """
    id: str
    title: str
    company_id: str

    # Content fields
    description: Optional[str]
    job_category: str
    skills: List[str]
    languages: List[Dict[str, str]]

    # Standard fields
    department_id: Optional[str]
    employment_type: Optional[str]
    experience_level: Optional[str]
    work_location_type: Optional[str]
    office_locations: List[str]
    remote_restrictions: Optional[str]
    number_of_openings: int

    # Salary fields (only if show_salary is True)
    salary_currency: Optional[str]
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    salary_period: Optional[str]

    # Visibility and publishing
    public_slug: Optional[str]
    application_deadline: Optional[date]
    published_at: Optional[datetime]

    # Custom fields (only candidate_visible ones)
    custom_fields: Dict[str, Any]

    @staticmethod
    def from_entity(entity: JobPosition) -> 'JobPositionPublicDto':
        """Create a public DTO from entity, filtering sensitive data"""
        # Convert languages to serializable format
        languages_data = LanguageRequirement.to_list(entity.languages) if entity.languages else []

        # Filter custom fields - only include candidate_visible ones
        visible_custom_fields = {}
        if entity.custom_fields_config and entity.custom_fields_values:
            visible_keys = {
                field.field_key for field in entity.custom_fields_config
                if field.candidate_visible and field.is_active
            }
            visible_custom_fields = {
                key: value for key, value in entity.custom_fields_values.items()
                if key in visible_keys
            }

        return JobPositionPublicDto(
            id=entity.id.value,
            title=entity.title,
            company_id=entity.company_id.value,
            # Content fields
            description=entity.description,
            job_category=entity.job_category.value,
            skills=entity.skills or [],
            languages=languages_data,
            # Standard fields
            department_id=entity.department_id,
            employment_type=entity.employment_type.value if entity.employment_type else None,
            experience_level=entity.experience_level.value if entity.experience_level else None,
            work_location_type=entity.work_location_type.value if entity.work_location_type else None,
            office_locations=entity.office_locations or [],
            remote_restrictions=entity.remote_restrictions,
            number_of_openings=entity.number_of_openings,
            # Salary fields - only if show_salary is True
            salary_currency=entity.salary_currency if entity.show_salary else None,
            salary_min=entity.salary_min if entity.show_salary else None,
            salary_max=entity.salary_max if entity.show_salary else None,
            salary_period=entity.salary_period.value if entity.show_salary and entity.salary_period else None,
            # Visibility and publishing
            public_slug=entity.public_slug,
            application_deadline=entity.application_deadline,
            published_at=entity.published_at,
            # Custom fields - only candidate visible
            custom_fields=visible_custom_fields
        )


@dataclass
class JobPositionStatsDto:
    """Job position statistics data transfer object"""
    total_positions: int = 0
    active_positions: int = 0
    inactive_positions: int = 0
    positions_by_type: Optional[Dict[str, int]] = None
    positions_by_company: Optional[Dict[str, int]] = None


@dataclass
class JobPositionListDto:
    """Job position list data transfer object"""
    positions: List[JobPositionDto]
    total: int
    page: int
    page_size: int
    total_pages: int
