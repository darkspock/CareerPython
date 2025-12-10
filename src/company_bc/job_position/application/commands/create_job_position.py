from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any, List

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.domain.entities.job_position import JobPosition
from src.company_bc.job_position.domain.enums import JobPositionVisibilityEnum
from src.company_bc.job_position.domain.exceptions import JobPositionInvalidScreeningTemplateError
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
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
class CreateJobPositionCommand(Command):
    id: JobPositionId
    company_id: CompanyId
    job_position_workflow_id: Optional[JobPositionWorkflowId] = None  # Workflow system
    stage_id: Optional[StageId] = None  # Initial stage
    phase_workflows: Optional[Dict[str, str]] = None
    custom_fields_config: Optional[List[CustomFieldDefinition]] = None  # Custom field definitions (from workflow)
    custom_fields_values: Optional[Dict[str, Any]] = None  # Custom field values
    source_workflow_id: Optional[str] = None  # Workflow ID from which custom fields were copied
    title: str = ""
    description: Optional[str] = None
    job_category: JobCategoryEnum = JobCategoryEnum.OTHER
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    visibility: JobPositionVisibilityEnum = JobPositionVisibilityEnum.HIDDEN
    public_slug: Optional[str] = None
    screening_template_id: Optional[str] = None  # Link to screening interview template


class CreateJobPositionCommandHandler(CommandHandler[CreateJobPositionCommand]):
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

    def execute(self, command: CreateJobPositionCommand) -> None:
        # Validate screening template if provided
        if command.screening_template_id:
            self._validate_screening_template(command.screening_template_id)

        job_position = JobPosition.create(
            id=command.id,
            company_id=command.company_id,
            job_position_workflow_id=command.job_position_workflow_id,
            stage_id=command.stage_id,
            phase_workflows=command.phase_workflows,
            custom_fields_config=command.custom_fields_config,
            custom_fields_values=command.custom_fields_values or {},
            source_workflow_id=command.source_workflow_id,
            title=command.title,
            description=command.description,
            job_category=command.job_category,
            open_at=command.open_at,
            application_deadline=command.application_deadline,
            visibility=command.visibility,
            public_slug=command.public_slug,
            screening_template_id=command.screening_template_id
        )

        self.job_position_repository.save(job_position)
