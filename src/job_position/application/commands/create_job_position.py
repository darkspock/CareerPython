from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any

from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.entities.job_position import JobPosition
from src.job_position.domain.enums import JobPositionVisibilityEnum
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.stage_id import StageId
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class CreateJobPositionCommand(Command):
    id: JobPositionId
    company_id: CompanyId
    job_position_workflow_id: Optional[JobPositionWorkflowId] = None  # Workflow system
    stage_id: Optional[StageId] = None  # Initial stage
    phase_workflows: Optional[Dict[str, str]] = None
    custom_fields_values: Optional[Dict[str, Any]] = None  # Custom field values (contains all removed fields)
    title: str = ""
    description: Optional[str] = None
    job_category: JobCategoryEnum = JobCategoryEnum.OTHER
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    visibility: JobPositionVisibilityEnum = JobPositionVisibilityEnum.HIDDEN
    public_slug: Optional[str] = None


class CreateJobPositionCommandHandler(CommandHandler[CreateJobPositionCommand]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: CreateJobPositionCommand) -> None:
        job_position = JobPosition.create(
            id=command.id,
            company_id=command.company_id,
            job_position_workflow_id=command.job_position_workflow_id,
            stage_id=command.stage_id,
            phase_workflows=command.phase_workflows,
            custom_fields_values=command.custom_fields_values or {},
            title=command.title,
            description=command.description,
            job_category=command.job_category,
            open_at=command.open_at,
            application_deadline=command.application_deadline,
            visibility=command.visibility,
            public_slug=command.public_slug
        )

        self.job_position_repository.save(job_position)
