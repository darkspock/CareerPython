"""Reorder Stages Command."""
from dataclasses import dataclass
from typing import List

from src.workflow.domain.exceptions.workflow_stage_not_found import WorkflowStageNotFound
from src.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared.application.command_bus import Command, CommandHandler


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
            WorkflowStageNotFound: If any stage doesn't exist
        """
        workflow_id = WorkflowId.from_string(command.workflow_id)

        # Get all stages for the workflow
        stages = self.repository.list_by_workflow(workflow_id)

        # Create a map of stage_id -> stage
        stage_map = {str(stage.id): stage for stage in stages}

        # Reorder stages according to the new order
        for new_order, stage_id_str in enumerate(command.stage_ids_in_order, start=1):
            if stage_id_str not in stage_map:
                raise WorkflowStageNotFound(f"Stage with id {stage_id_str} not found")

            stage = stage_map[stage_id_str]
            # reorder() modifies the instance directly (mutability)
            stage.reorder(new_order)
            self.repository.save(stage)
