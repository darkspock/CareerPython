from dataclasses import dataclass
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any, List

from src.company_bc.job_position.domain.enums import (
    JobPositionVisibilityEnum,
    EmploymentTypeEnum,
    ExperienceLevelEnum,
    WorkLocationTypeEnum,
    SalaryPeriodEnum,
)
from src.company_bc.job_position.domain.exceptions import (
    JobPositionNotFoundException,
    JobPositionInvalidScreeningTemplateError
)
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.company_bc.job_position.domain.value_objects.language_requirement import LanguageRequirement
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.interview_bc.interview_template.domain.enums import InterviewTemplateScopeEnum
from src.interview_bc.interview_template.domain.infrastructure.interview_template_repository_interface import \
    InterviewTemplateRepositoryInterface
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateId


@dataclass
class UpdateJobPositionCommand(Command):
    id: JobPositionId
    job_position_workflow_id: Optional[JobPositionWorkflowId] = None
    stage_id: Optional[StageId] = None
    phase_workflows: Optional[Dict[str, str]] = None
    custom_fields_values: Optional[Dict[str, Any]] = None
    title: str = ""
    description: Optional[str] = None
    job_category: Optional[JobCategoryEnum] = None
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    visibility: Optional[JobPositionVisibilityEnum] = None
    public_slug: Optional[str] = None
    screening_template_id: Optional[str] = None
    # Job details fields
    skills: Optional[List[str]] = None
    languages: Optional[List[LanguageRequirement]] = None
    department_id: Optional[str] = None
    employment_type: Optional[EmploymentTypeEnum] = None
    experience_level: Optional[ExperienceLevelEnum] = None
    work_location_type: Optional[WorkLocationTypeEnum] = None
    office_locations: Optional[List[str]] = None
    remote_restrictions: Optional[str] = None
    number_of_openings: Optional[int] = None
    requisition_id: Optional[str] = None
    # Financial fields
    salary_currency: Optional[str] = None
    salary_min: Optional[Decimal] = None
    salary_max: Optional[Decimal] = None
    salary_period: Optional[SalaryPeriodEnum] = None
    show_salary: Optional[bool] = None
    budget_max: Optional[Decimal] = None
    # Ownership fields
    hiring_manager_id: Optional[str] = None
    recruiter_id: Optional[str] = None
    # Custom fields config (position-specific field definitions)
    custom_fields_config: Optional[List[CustomFieldDefinition]] = None
    # Killer questions (simple inline questions stored as JSON)
    killer_questions: Optional[List[Dict[str, Any]]] = None


class UpdateJobPositionCommandHandler(CommandHandler[UpdateJobPositionCommand]):
    def __init__(
        self,
        job_position_repository: JobPositionRepositoryInterface,
        interview_template_repository: Optional[InterviewTemplateRepositoryInterface] = None
    ):
        self.job_position_repository = job_position_repository
        self.interview_template_repository = interview_template_repository

    def _validate_screening_template(self, template_id: str) -> None:
        """Validate that screening template exists and has scope=APPLICATION"""
        if not self.interview_template_repository:
            return  # Skip validation if repository not provided

        template = self.interview_template_repository.get_by_id(
            InterviewTemplateId.from_string(template_id)
        )
        if not template:
            raise JobPositionInvalidScreeningTemplateError(
                template_id, "Template not found"
            )
        if template.scope != InterviewTemplateScopeEnum.APPLICATION:
            raise JobPositionInvalidScreeningTemplateError(
                template_id,
                f"Template scope must be APPLICATION, got {template.scope.value}"
            )

    def execute(self, command: UpdateJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        # Validate screening template if provided and changed
        if command.screening_template_id and command.screening_template_id != job_position.screening_template_id:
            self._validate_screening_template(command.screening_template_id)

        job_position.update_details(
            title=command.title,
            description=command.description,
            job_category=command.job_category or job_position.job_category,
            open_at=command.open_at,
            application_deadline=command.application_deadline,
            job_position_workflow_id=command.job_position_workflow_id,
            stage_id=command.stage_id,
            phase_workflows=command.phase_workflows,
            custom_fields_values=command.custom_fields_values,
            visibility=command.visibility,
            public_slug=command.public_slug,
            screening_template_id=command.screening_template_id,
            # Job details fields
            skills=command.skills,
            languages=command.languages,
            department_id=command.department_id,
            employment_type=command.employment_type,
            experience_level=command.experience_level,
            work_location_type=command.work_location_type,
            office_locations=command.office_locations,
            remote_restrictions=command.remote_restrictions,
            number_of_openings=command.number_of_openings,
            requisition_id=command.requisition_id,
            # Financial fields
            salary_currency=command.salary_currency,
            salary_min=command.salary_min,
            salary_max=command.salary_max,
            salary_period=command.salary_period,
            show_salary=command.show_salary,
            budget_max=command.budget_max,
            # Custom fields config
            custom_fields_config=command.custom_fields_config,
            # Killer questions
            killer_questions=command.killer_questions,
        )

        self.job_position_repository.save(job_position)
