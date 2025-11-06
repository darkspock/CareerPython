from dataclasses import dataclass
from typing import Optional, Dict, Any, List

from src.job_position.domain.enums.job_position_workflow_status import JobPositionWorkflowStatusEnum
from src.job_position.domain.enums.view_type import ViewTypeEnum
from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import \
    JobPositionWorkflowRepositoryInterface
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class UpdateJobPositionWorkflowCommand(Command):
    """Command to update a job position workflow"""
    id: JobPositionWorkflowId
    name: str
    default_view: Optional[ViewTypeEnum] = None
    status: Optional[JobPositionWorkflowStatusEnum] = None
    stages: Optional[List[WorkflowStage]] = None
    custom_fields_config: Optional[Dict[str, Any]] = None


class UpdateJobPositionWorkflowCommandHandler(CommandHandler[UpdateJobPositionWorkflowCommand]):
    """Handler for updating a job position workflow"""

    def __init__(self, workflow_repository: JobPositionWorkflowRepositoryInterface):
        self.workflow_repository = workflow_repository

    def execute(self, command: UpdateJobPositionWorkflowCommand) -> None:
        """Execute the command - updates an existing workflow"""
        workflow = self.workflow_repository.get_by_id(command.id)
        if not workflow:
            raise JobPositionNotFoundException(f"Workflow with id {command.id.value} not found")

        workflow.update(
            name=command.name,
            default_view=command.default_view,
            status=command.status,
            custom_fields_config=command.custom_fields_config,
        )

        # Update stages if provided
        if command.stages is not None:
            # Remove all existing stages
            stage_ids_to_remove = [stage.id.value for stage in workflow.stages]
            for stage_id in stage_ids_to_remove:
                try:
                    workflow.remove_stage(stage_id)
                except ValueError:
                    pass  # Stage might already be removed

            # Add/update stages
            for stage in command.stages:
                # Check if stage exists
                existing_stage = workflow.get_stage_by_id(stage.id.value)
                if existing_stage:
                    # Update existing stage
                    workflow.update_stage(stage.id.value, stage)
                else:
                    # Add new stage
                    workflow.add_stage(stage)

        self.workflow_repository.save(workflow)
