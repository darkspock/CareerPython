"""Delete Stage Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.delete_stage_command import DeleteStageCommand
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.exceptions.stage_not_found import StageNotFound


class DeleteStageCommandHandler(CommandHandler[DeleteStageCommand, None]):
    """Handler for deleting a workflow stage."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, command: DeleteStageCommand) -> None:
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
