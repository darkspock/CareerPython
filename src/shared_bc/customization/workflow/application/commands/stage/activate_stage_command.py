"""Activate Stage Command."""
from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.exceptions.workflow_stage_not_found import WorkflowStageNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class ActivateStageCommand(Command):
    """Command to activate a workflow stage."""

    id: WorkflowStageId


class ActivateStageCommandHandler(CommandHandler[ActivateStageCommand]):
    """Handler for activating a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: ActivateStageCommand) -> None:
        """
        Handle the activate stage command.

        Args:
            command: The activate stage command

        Raises:
            WorkflowStageNotFound: If stage doesn't exist
        """
        stage = self.repository.get_by_id(command.id)

        if not stage:
            raise WorkflowStageNotFound(f"Stage with id {command.id} not found")

        # activate() modifies the instance directly (mutability)
        stage.activate()
        self.repository.save(stage)
