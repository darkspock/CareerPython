import logging
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any, List

from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.enums import JobPositionStatusEnum, ContractTypeEnum, WorkLocationTypeEnum
from src.job_position.domain.enums.employment_type import EmploymentType
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.job_position.domain.exceptions.job_position_exceptions import JobPositionValidationError
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.job_position.domain.value_objects.salary_range import SalaryRange
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPosition:
    """Job position domain entity"""
    id: JobPositionId
    title: str
    company_id: CompanyId
    workflow_id: Optional[str]  # Legacy/default workflow
    phase_workflows: Optional[Dict[str, str]]  # Phase 12.8: phase_id -> workflow_id mapping
    description: Optional[str]
    location: Optional[str]
    employment_type: Optional[EmploymentType]
    work_location_type: WorkLocationTypeEnum
    salary_range: Optional[SalaryRange]
    contract_type: ContractTypeEnum
    requirements: Optional[Dict[str, Any]]
    job_category: JobCategoryEnum
    position_level: Optional[JobPositionLevelEnum]
    number_of_openings: int
    application_instructions: Optional[str]
    benefits: List[str]
    working_hours: Optional[str]
    travel_required: Optional[int]
    languages_required: Dict[LanguageEnum, LanguageLevelEnum]
    visa_sponsorship: bool
    contact_person: Optional[str]
    department: Optional[str]
    reports_to: Optional[str]
    status: JobPositionStatusEnum
    desired_roles: Optional[List[PositionRoleEnum]]
    open_at: Optional[datetime]
    application_deadline: Optional[date]
    skills: List[str]
    application_url: Optional[str]
    application_email: Optional[str]
    is_public: bool
    public_slug: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def __post_init__(self) -> None:
        """Clean up duplicates after initialization"""
        # Clean duplicates in lists and dicts
        if self.desired_roles:
            self.desired_roles = self._remove_duplicate_roles(self.desired_roles)
        if self.languages_required:
            self.languages_required = self._remove_duplicate_languages(self.languages_required)
        if self.skills:
            self.skills = self._remove_duplicate_strings(self.skills)
        if self.benefits:
            self.benefits = self._remove_duplicate_strings(self.benefits)

    @staticmethod
    def _remove_duplicate_roles(roles: List[PositionRoleEnum]) -> List[PositionRoleEnum]:
        """Remove duplicate roles while preserving order"""
        if not roles:
            return roles

        seen = set()
        unique_roles = []
        for role in roles:
            if role not in seen:
                unique_roles.append(role)
                seen.add(role)
            else:
                logging.getLogger(__name__).warning(f"Duplicate role '{role.value}' removed")

        return unique_roles

    @staticmethod
    def _remove_duplicate_languages(languages: Dict[LanguageEnum, LanguageLevelEnum]) -> Dict[LanguageEnum, LanguageLevelEnum]:
        """Remove duplicate languages (dict keys are already unique, but this is for consistency)"""
        # Dict keys are inherently unique, but we might want to add validation here
        if not languages:
            return languages

        # Could add validation for conflicting levels for same language here if needed
        return languages

    @staticmethod
    def _remove_duplicate_strings(string_list: List[str]) -> List[str]:
        """Remove duplicate strings while preserving order"""
        if not string_list:
            return string_list

        seen = set()
        unique_strings = []
        for item in string_list:
            item_clean = item.strip()
            if item_clean and item_clean.lower() not in seen:
                unique_strings.append(item)
                seen.add(item_clean.lower())
            elif item_clean:
                logging.getLogger(__name__).warning(f"Duplicate item '{item}' removed")

        return unique_strings

    def submit_for_approval(self) -> None:
        """Submit job position for approval"""
        if self.status in [JobPositionStatusEnum.PENDING, JobPositionStatusEnum.APPROVED]:
            return

        # Validate required fields for submission
        if not self.description:
            raise JobPositionValidationError("Description is required for submission")

        self.status = JobPositionStatusEnum.PENDING
        self.updated_at = datetime.utcnow()

    def approve(self) -> None:
        """Approve the job position"""
        if self.status == JobPositionStatusEnum.APPROVED:
            return
        self.status = JobPositionStatusEnum.APPROVED
        self.updated_at = datetime.utcnow()

    def reject(self) -> None:
        """Reject the job position"""
        if self.status == JobPositionStatusEnum.REJECTED:
            return
        self.status = JobPositionStatusEnum.REJECTED
        self.updated_at = datetime.utcnow()

    def open_position(self) -> None:
        """Open the job position for applications (only if approved)"""
        if self.status != JobPositionStatusEnum.APPROVED:
            raise JobPositionValidationError("Job position must be approved before opening")
        self.status = JobPositionStatusEnum.OPEN
        self.updated_at = datetime.utcnow()

    def close_position(self) -> None:
        """Close the job position"""
        if self.status == JobPositionStatusEnum.CLOSED:
            return
        self.status = JobPositionStatusEnum.CLOSED
        self.updated_at = datetime.utcnow()

    def pause_position(self) -> None:
        """Pause the job position"""
        if self.status not in [JobPositionStatusEnum.OPEN]:
            raise JobPositionValidationError("Only open positions can be paused")
        self.status = JobPositionStatusEnum.PAUSED
        self.updated_at = datetime.utcnow()

    def resume_position(self) -> None:
        """Resume a paused job position"""
        if self.status != JobPositionStatusEnum.PAUSED:
            raise JobPositionValidationError("Only paused positions can be resumed")
        self.status = JobPositionStatusEnum.OPEN
        self.updated_at = datetime.utcnow()

    def is_approved(self) -> bool:
        """Check if job position is approved"""
        return self.status == JobPositionStatusEnum.APPROVED

    def is_open(self) -> bool:
        """Check if job position is open for applications"""
        return self.status == JobPositionStatusEnum.OPEN

    def can_receive_applications(self) -> bool:
        """Check if job position can receive applications"""
        return self.status == JobPositionStatusEnum.OPEN

    def is_pending(self) -> bool:
        """Check if job position is in draft state"""
        return self.status == JobPositionStatusEnum.PENDING

    def get_workflow_for_phase(self, phase_id: str) -> Optional[str]:
        """Get the workflow ID configured for a specific phase

        Phase 12.8: Returns the workflow_id configured for the given phase.
        If no phase-specific workflow is configured, returns the default workflow_id.
        """
        if self.phase_workflows and phase_id in self.phase_workflows:
            return self.phase_workflows[phase_id]
        return self.workflow_id  # Fallback to default/legacy workflow

    def add_requirement(self, requirement_type: str, requirement_data: Any) -> None:
        """Add a requirement to the job position"""
        if self.requirements is None:
            self.requirements = {}

        if requirement_type not in ["technical_skills", "soft_skills", "experience", "education", "certifications"]:
            raise JobPositionValidationError(f"Invalid requirement type: {requirement_type}")

        self.requirements[requirement_type] = requirement_data
        self.updated_at = datetime.utcnow()

    def remove_requirement(self, requirement_type: str) -> None:
        """Remove a requirement from the job position"""
        if self.requirements and requirement_type in self.requirements:
            del self.requirements[requirement_type]
            self.updated_at = datetime.utcnow()

    def update_details(
            self,
            workflow_id: Optional[str],
            phase_workflows: Optional[Dict[str, str]],
            title: str,
            description: Optional[str],
            location: Optional[str],
            employment_type: Optional[EmploymentType],
            work_location_type: WorkLocationTypeEnum,
            salary_range: Optional[SalaryRange],
            contract_type: ContractTypeEnum,
            requirements: Dict[str, Any],
            job_category: JobCategoryEnum,
            position_level: Optional[JobPositionLevelEnum],
            number_of_openings: int,
            application_instructions: Optional[str],
            benefits: List[str],
            working_hours: Optional[str],
            travel_required: Optional[int],
            languages_required: Dict[LanguageEnum, LanguageLevelEnum],
            visa_sponsorship: bool,
            contact_person: Optional[str],
            department: Optional[str],
            reports_to: Optional[str],
            desired_roles: Optional[List[PositionRoleEnum]],
            open_at: Optional[datetime],
            application_deadline: Optional[date],
            skills: List[str],
            application_url: Optional[str],
            application_email: Optional[str]
    ) -> None:
        """Update job position details with all attributes"""
        # Validate required fields
        if not title or title.strip() == "":
            raise JobPositionValidationError("Title is required")

        if number_of_openings < 1:
            raise JobPositionValidationError("Number of openings must be at least 1")

        if travel_required is not None and (travel_required < 0 or travel_required > 100):
            raise JobPositionValidationError("Travel required must be between 0 and 100")

        self.workflow_id = workflow_id
        self.phase_workflows = phase_workflows or {}
        self.title = title.strip()
        self.description = description
        self.location = location
        self.employment_type = employment_type
        self.work_location_type = work_location_type
        self.salary_range = salary_range
        self.contract_type = contract_type
        self.requirements = requirements or {}
        self.job_category = job_category
        self.position_level = position_level
        self.number_of_openings = number_of_openings
        self.application_instructions = application_instructions
        self.benefits = benefits or []
        self.working_hours = working_hours
        self.travel_required = travel_required
        self.languages_required = languages_required or {}
        self.visa_sponsorship = visa_sponsorship
        self.contact_person = contact_person
        self.department = department
        self.reports_to = reports_to
        self.desired_roles = desired_roles
        self.open_at = open_at
        self.application_deadline = application_deadline
        self.skills = skills or []
        self.application_url = application_url
        self.application_email = application_email
        self.updated_at = datetime.utcnow()

    @staticmethod
    def create(
            id: JobPositionId,
            title: str,
            company_id: CompanyId,
            workflow_id: Optional[str] = None,
            phase_workflows: Optional[Dict[str, str]] = None,
            description: Optional[str] = None,
            location: Optional[str] = None,
            employment_type: Optional[EmploymentType] = None,
            work_location_type: WorkLocationTypeEnum = WorkLocationTypeEnum.ON_SITE,
            salary_range: Optional[SalaryRange] = None,
            contract_type: ContractTypeEnum = ContractTypeEnum.FULL_TIME,
            requirements: Optional[Dict[str, Any]] = None,
            job_category: JobCategoryEnum = JobCategoryEnum.OTHER,
            position_level: Optional[JobPositionLevelEnum] = None,
            number_of_openings: int = 1,
            application_instructions: Optional[str] = None,
            benefits: Optional[List[str]] = None,
            working_hours: Optional[str] = None,
            travel_required: Optional[int] = None,
            languages_required: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None,
            visa_sponsorship: bool = False,
            contact_person: Optional[str] = None,
            department: Optional[str] = None,
            reports_to: Optional[str] = None,
            desired_roles: Optional[List[PositionRoleEnum]] = None,
            open_at: Optional[datetime] = None,
            application_deadline: Optional[date] = None,
            application_url: Optional[str] = None,
            application_email: Optional[str] = None,
            skills: Optional[List[str]] = None
    ) -> 'JobPosition':
        """Create a new job position"""
        now = datetime.utcnow()

        return JobPosition(
            id=id,
            title=title,
            company_id=company_id,
            workflow_id=workflow_id,
            phase_workflows=phase_workflows or {},
            description=description,
            location=location,
            employment_type=employment_type,
            work_location_type=work_location_type,
            salary_range=salary_range,
            contract_type=contract_type,
            requirements=requirements or {},
            job_category=job_category,
            position_level=position_level,
            number_of_openings=number_of_openings,
            application_instructions=application_instructions,
            benefits=benefits or [],
            working_hours=working_hours,
            travel_required=travel_required,
            languages_required=languages_required or {},
            visa_sponsorship=visa_sponsorship,
            contact_person=contact_person,
            department=department,
            reports_to=reports_to,
            status=JobPositionStatusEnum.PENDING,
            desired_roles=desired_roles,
            open_at=open_at,
            application_deadline=application_deadline,
            skills=skills or [],
            application_url=application_url,
            application_email=application_email,
            created_at=now,
            updated_at=now
        )

    @classmethod
    def _from_repository(
            cls,
            id: JobPositionId,
            title: str,
            company_id: CompanyId,
            workflow_id: Optional[str],
            phase_workflows: Optional[Dict[str, str]],
            description: Optional[str],
            location: Optional[str],
            employment_type: Optional[EmploymentType],
            work_location_type: WorkLocationTypeEnum,
            salary_range: Optional[SalaryRange],
            contract_type: ContractTypeEnum,
            requirements: Optional[Dict[str, Any]],
            job_category: JobCategoryEnum,
            position_level: Optional[JobPositionLevelEnum],
            number_of_openings: int,
            application_instructions: Optional[str],
            benefits: List[str],
            working_hours: Optional[str],
            travel_required: Optional[int],
            languages_required: Dict[LanguageEnum, LanguageLevelEnum],
            visa_sponsorship: bool,
            contact_person: Optional[str],
            department: Optional[str],
            reports_to: Optional[str],
            status: JobPositionStatusEnum,
            desired_roles: Optional[List[PositionRoleEnum]],
            open_at: Optional[datetime],
            application_deadline: Optional[date],
            skills: List[str],
            application_url: Optional[str],
            application_email: Optional[str],
            created_at: datetime,
            updated_at: datetime
    ) -> 'JobPosition':
        """Create JobPosition from repository data - only for repositories to use"""
        return cls(
            id=id,
            title=title,
            company_id=company_id,
            workflow_id=workflow_id,
            phase_workflows=phase_workflows,
            description=description,
            location=location,
            employment_type=employment_type,
            work_location_type=work_location_type,
            salary_range=salary_range,
            contract_type=contract_type,
            requirements=requirements,
            job_category=job_category,
            position_level=position_level,
            number_of_openings=number_of_openings,
            application_instructions=application_instructions,
            benefits=benefits,
            working_hours=working_hours,
            travel_required=travel_required,
            languages_required=languages_required,
            visa_sponsorship=visa_sponsorship,
            contact_person=contact_person,
            department=department,
            reports_to=reports_to,
            status=status,
            desired_roles=desired_roles,
            open_at=open_at,
            application_deadline=application_deadline,
            skills=skills,
            application_url=application_url,
            application_email=application_email,
            created_at=created_at,
            updated_at=updated_at
        )
