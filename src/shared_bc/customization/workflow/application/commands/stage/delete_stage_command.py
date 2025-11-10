"""Delete Stage Command."""
from dataclasses import dataclass

from src.shared_bc.customization.workflow.domain.exceptions.workflow_stage_not_found import WorkflowStageNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteStageCommand(Command):
    """Command to delete a workflow stage."""

    id: WorkflowStageId


class DeleteStageCommandHandler(CommandHandler[DeleteStageCommand]):
    """Handler for deleting a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteStageCommand) -> None:
        """
        Handle the delete stage command.

        Args:
            command: The delete stage command

        Raises:
            WorkflowStageNotFound: If stage doesn't exist
        """
        stage = self.repository.get_by_id(command.id)

        if not stage:
            raise WorkflowStageNotFound(f"Stage with id {command.id} not found")

        self.repository.delete(command.id)
