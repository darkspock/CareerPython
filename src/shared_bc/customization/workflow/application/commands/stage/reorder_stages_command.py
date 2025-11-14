"""Reorder Stages Command."""
from dataclasses import dataclass
from typing import List

from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.exceptions.workflow_stage_not_found import WorkflowStageNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class ReorderStagesCommand(Command):
    """Command to reorder stages in a workflow."""

    workflow_id: WorkflowId
    stage_ids_in_order: List[WorkflowStageId]


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
            WorkflowStageNotFound: If any stage doesn't exist
        """
        # Get all stages for the workflow
        stages = self.repository.list_by_workflow(command.workflow_id)

        # Create a map of stage_id -> stage
        stage_map = {stage.id: stage for stage in stages}

        # Reorder stages according to the new order
        for new_order, stage_id in enumerate(command.stage_ids_in_order, start=1):
            if stage_id not in stage_map:
                raise WorkflowStageNotFound(f"Stage with id {stage_id} not found")

            stage = stage_map[stage_id]
            # reorder() modifies the instance directly (mutability)
            stage.reorder(new_order)
            self.repository.save(stage)
