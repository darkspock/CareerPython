"""Delete Stage Command."""
from dataclasses import dataclass
from src.shared.application.command_bus import Command, CommandHandler
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound


@dataclass(frozen=True)
class DeleteStageCommand(Command):
    """Command to delete a workflow stage."""

    id: str


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
            StageNotFound: If stage doesn't exist
        """
        stage_id = WorkflowStageId.from_string(command.id)
        stage = self.repository.get_by_id(stage_id)

        if not stage:
            raise StageNotFound(f"Stage with id {command.id} not found")

        self.repository.delete(stage_id)