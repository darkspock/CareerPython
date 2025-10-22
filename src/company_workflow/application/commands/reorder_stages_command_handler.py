"""Reorder Stages Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.reorder_stages_command import ReorderStagesCommand
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound


class ReorderStagesCommandHandler(CommandHandler[ReorderStagesCommand, None]):
    """Handler for reordering stages in a workflow."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, command: ReorderStagesCommand) -> None:
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
