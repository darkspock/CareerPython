"""Deactivate Stage Command."""
from dataclasses import dataclass

from src.shared_bc.customization.workflow.domain.exceptions.workflow_stage_not_found import WorkflowStageNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeactivateStageCommand(Command):
    """Command to deactivate a workflow stage."""

    id: WorkflowStageId


class DeactivateStageCommandHandler(CommandHandler[DeactivateStageCommand]):
    """Handler for deactivating a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeactivateStageCommand) -> None:
        """
        Handle the deactivate stage command.

        Args:
            command: The deactivate stage command

        Raises:
            WorkflowStageNotFound: If stage doesn't exist
        """
        stage = self.repository.get_by_id(command.id)

        if not stage:
            raise WorkflowStageNotFound(f"Stage with id {command.id} not found")

        # deactivate() modifies the instance directly (mutability)
        stage.deactivate()
        self.repository.save(stage)
