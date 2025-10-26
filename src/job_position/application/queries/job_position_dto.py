"""Job position DTOs"""
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, List, Dict, Any

from src.candidate.domain.enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain import JobPosition, WorkLocationTypeEnum, SalaryRange, ContractTypeEnum, \
    JobPositionStatusEnum
from src.job_position.domain.enums.employment_type import EmploymentType
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.job_position.domain.value_objects import JobPositionId
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPositionDto:
    id: JobPositionId
    title: str
    company_id: CompanyId
    workflow_id: Optional[str]
    description: Optional[str]
    position_level: Optional[JobPositionLevelEnum]
    location: Optional[str]
    employment_type: Optional[EmploymentType]
    work_location_type: WorkLocationTypeEnum
    salary_range: Optional[SalaryRange]
    contract_type: ContractTypeEnum
    requirements: Optional[Dict[str, Any]]
    job_category: JobCategoryEnum
    number_of_openings: int
    application_instructions: Optional[str]
    benefits: List[str]
    working_hours: Optional[str]  # e.g., "40h/week", "flexible"
    travel_required: Optional[int]  # percentage (0-100)
    languages_required: Dict[LanguageEnum, LanguageLevelEnum]
    visa_sponsorship: bool
    contact_person: Optional[str]
    department: Optional[str]
    reports_to: Optional[str]
    status: JobPositionStatusEnum
    desired_roles: Optional[List[PositionRoleEnum]]
    open_at: Optional[datetime]
    application_deadline: Optional[date]
    application_url: Optional[str]
    application_email: Optional[str]
    skills: List[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    @staticmethod
    def from_entity(entity: JobPosition) -> 'JobPositionDto':
        """Create a JobPositionDto from a JobPosition entity"""
        return JobPositionDto(
            id=entity.id,
            company_id=entity.company_id,
            workflow_id=entity.workflow_id,
            work_location_type=entity.work_location_type,
            salary_range=entity.salary_range,
            contract_type=entity.contract_type,
            job_category=entity.job_category,
            position_level=entity.position_level,
            number_of_openings=entity.number_of_openings,
            application_instructions=entity.application_instructions,
            working_hours=entity.working_hours,
            travel_required=entity.travel_required,
            languages_required=entity.languages_required,
            visa_sponsorship=entity.visa_sponsorship,
            contact_person=entity.contact_person,
            status=entity.status,
            desired_roles=entity.desired_roles,
            open_at=entity.open_at,
            title=entity.title,
            description=entity.description,
            location=entity.location,
            employment_type=entity.employment_type,
            department=entity.department,
            reports_to=entity.reports_to,
            requirements=entity.requirements or None,
            benefits=entity.benefits or [],
            application_deadline=entity.application_deadline,
            application_url=entity.application_url,
            application_email=entity.application_email,
            skills=entity.skills or [],
            created_at=entity.created_at,
            updated_at=entity.updated_at
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
