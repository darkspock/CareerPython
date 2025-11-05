from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.shared.application.command_bus import Command, CommandHandler
from src.job_position.domain.entities.job_position_workflow import JobPositionWorkflow
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.enums.job_position_workflow_status import JobPositionWorkflowStatusEnum
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import JobPositionWorkflowRepositoryInterface


@dataclass
class CreateJobPositionWorkflowCommand(Command):
    """Command to create a new job position workflow"""
    id: JobPositionWorkflowId
    company_id: CompanyId
    name: str
    default_view: ViewTypeEnum = ViewTypeEnum.KANBAN
    status: Optional[JobPositionWorkflowStatusEnum] = None  # If None, uses default from entity (DRAFT)
    stages: Optional[List[WorkflowStage]] = None
    custom_fields_config: Optional[Dict[str, Any]] = None


class CreateJobPositionWorkflowCommandHandler(CommandHandler[CreateJobPositionWorkflowCommand]):
    """Handler for creating a job position workflow"""

    def __init__(self, workflow_repository: JobPositionWorkflowRepositoryInterface):
        self.workflow_repository = workflow_repository

    def execute(self, command: CreateJobPositionWorkflowCommand) -> None:
        """Execute the command - creates a new workflow"""
        # If status is explicitly provided, use it; otherwise use default from entity (DRAFT)
        if command.status is not None:
            workflow = JobPositionWorkflow.create(
                id=command.id,
                company_id=command.company_id,
                name=command.name,
                default_view=command.default_view,
                status=command.status,
                stages=command.stages,
                custom_fields_config=command.custom_fields_config,
            )
        else:
            workflow = JobPositionWorkflow.create(
                id=command.id,
                company_id=command.company_id,
                name=command.name,
                default_view=command.default_view,
                stages=command.stages,
                custom_fields_config=command.custom_fields_config,
            )

        self.workflow_repository.save(workflow)

