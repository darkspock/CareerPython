from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any, List

from src.candidate.domain.enums.candidate_enums import LanguageEnum, LanguageLevelEnum, PositionRoleEnum
from src.job_position.domain.enums import WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.domain.enums.employment_type import EmploymentType
from src.job_position.domain.enums.position_level_enum import JobPositionLevelEnum
from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.salary_range import SalaryRange
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class UpdateJobPositionCommand(Command):
    id: JobPositionId
    workflow_id: Optional[str] = None
    phase_workflows: Optional[Dict[str, str]] = None
    title: str = ""
    description: Optional[str] = None
    location: Optional[str] = None
    employment_type: Optional[EmploymentType] = None
    work_location_type: WorkLocationTypeEnum = WorkLocationTypeEnum.ON_SITE
    salary_range: Optional[SalaryRange] = None
    contract_type: ContractTypeEnum = ContractTypeEnum.FULL_TIME
    requirements: Optional[Dict[str, Any]] = None
    job_category: JobCategoryEnum = JobCategoryEnum.OTHER
    position_level: Optional[JobPositionLevelEnum] = None
    number_of_openings: int = 1
    application_instructions: Optional[str] = None
    benefits: Optional[List[str]] = None
    working_hours: Optional[str] = None
    travel_required: Optional[int] = None
    languages_required: Optional[Dict[LanguageEnum, LanguageLevelEnum]] = None
    visa_sponsorship: bool = False
    contact_person: Optional[str] = None
    department: Optional[str] = None
    reports_to: Optional[str] = None
    desired_roles: Optional[List[PositionRoleEnum]] = None
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    skills: Optional[List[str]] = None
    application_url: Optional[str] = None
    application_email: Optional[str] = None
    is_public: Optional[bool] = None


class UpdateJobPositionCommandHandler(CommandHandler[UpdateJobPositionCommand]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: UpdateJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.update_details(
            workflow_id=command.workflow_id,
            phase_workflows=command.phase_workflows,
            title=command.title,
            description=command.description,
            location=command.location,
            employment_type=command.employment_type,
            work_location_type=command.work_location_type,
            salary_range=command.salary_range,
            contract_type=command.contract_type,
            requirements=command.requirements or {},
            job_category=command.job_category,
            position_level=command.position_level,
            number_of_openings=command.number_of_openings,
            application_instructions=command.application_instructions,
            benefits=command.benefits or [],
            working_hours=command.working_hours,
            travel_required=command.travel_required,
            languages_required=command.languages_required or {},
            visa_sponsorship=command.visa_sponsorship,
            contact_person=command.contact_person,
            department=command.department,
            reports_to=command.reports_to,
            desired_roles=command.desired_roles,
            open_at=command.open_at,
            application_deadline=command.application_deadline,
            skills=command.skills or [],
            application_url=command.application_url,
            application_email=command.application_email,
            is_public=command.is_public
        )

        # When publishing (is_public=True), automatically approve and open the position
        # so it appears in public listings
        if command.is_public is True and not job_position.is_open():
            # First approve if not already approved
            if not job_position.is_approved():
                job_position.approve()
            # Then open the position
            job_position.open_position()

        self.job_position_repository.save(job_position)
