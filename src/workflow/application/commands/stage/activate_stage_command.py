"""Activate Stage Command."""
from dataclasses import dataclass

from src.workflow.domain.exceptions.stage_not_found import StageNotFound
from src.workflow.domain.infrastructure.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ActivateStageCommand(Command):
    """Command to activate a workflow stage."""

    id: str


class ActivateStageCommandHandler(CommandHandler):
    """Handler for activating a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: ActivateStageCommand) -> None:
        """
        Handle the activate stage command.

        Args:
            command: The activate stage command

        Raises:
            StageNotFound: If stage doesn't exist
        """
        stage_id = WorkflowStageId.from_string(command.id)
        stage = self.repository.get_by_id(stage_id)

        if not stage:
            raise StageNotFound(f"Stage with id {command.id} not found")

        activated_stage = stage.activate()
        self.repository.save(activated_stage)
