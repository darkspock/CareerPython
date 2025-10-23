"""Reorder Stages Command."""
from dataclasses import dataclass
from typing import List
from src.shared.application.command_bus import Command, CommandHandler
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound


@dataclass(frozen=True)
class ReorderStagesCommand(Command):
    """Command to reorder stages in a workflow."""

    workflow_id: str
    stage_ids_in_order: List[str]


class ReorderStagesCommandHandler(CommandHandler[ReorderStagesCommand]):
    """Handler for reordering stages in a workflow."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: ReorderStagesCommand) -> None:
        """
        Handle the reorder stages command.

        Args:
            command: The reorder stages command

        Raises:
            StageNotFound: If any stage doesn't exist
        """
        workflow_id = CompanyWorkflowId.from_string(command.workflow_id)

        # Get all stages for the workflow
        stages = self.repository.list_by_workflow(workflow_id)

        # Create a map of stage_id -> stage
        stage_map = {stage.id.value: stage for stage in stages}

        # Reorder stages according to the new order
        for new_order, stage_id_str in enumerate(command.stage_ids_in_order, start=1):
            if stage_id_str not in stage_map:
                raise StageNotFound(f"Stage with id {stage_id_str} not found")

            stage = stage_map[stage_id_str]
            reordered_stage = stage.reorder(new_order)
            self.repository.save(reordered_stage)