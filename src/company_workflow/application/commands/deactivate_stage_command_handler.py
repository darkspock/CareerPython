"""Deactivate Stage Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.deactivate_stage_command import DeactivateStageCommand
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound


class DeactivateStageCommandHandler(CommandHandler[DeactivateStageCommand, None]):
    """Handler for deactivating a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, command: DeactivateStageCommand) -> None:
        """
        Handle the deactivate stage command.

        Args:
            command: The deactivate stage command

        Raises:
            StageNotFound: If stage doesn't exist
        """
        stage_id = WorkflowStageId.from_string(command.id)
        stage = self.repository.get_by_id(stage_id)

        if not stage:
            raise StageNotFound(f"Stage with id {command.id} not found")

        deactivated_stage = stage.deactivate()
        self.repository.save(deactivated_stage)
