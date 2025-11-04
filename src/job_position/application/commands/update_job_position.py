from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any

from src.job_position.domain.enums import JobPositionVisibilityEnum
from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.stage_id import StageId
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class UpdateJobPositionCommand(Command):
    id: JobPositionId
    job_position_workflow_id: Optional[JobPositionWorkflowId] = None  # Workflow system
    stage_id: Optional[StageId] = None  # Current stage
    phase_workflows: Optional[Dict[str, str]] = None
    custom_fields_values: Optional[Dict[str, Any]] = None  # Custom field values (contains all removed fields)
    title: str = ""
    description: Optional[str] = None
    job_category: Optional[JobCategoryEnum] = None
    open_at: Optional[datetime] = None
    application_deadline: Optional[date] = None
    visibility: Optional[JobPositionVisibilityEnum] = None
    public_slug: Optional[str] = None


class UpdateJobPositionCommandHandler(CommandHandler[UpdateJobPositionCommand]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: UpdateJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

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
            public_slug=command.public_slug
        )

        self.job_position_repository.save(job_position)
