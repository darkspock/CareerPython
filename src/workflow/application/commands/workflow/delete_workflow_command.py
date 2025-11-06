"""Delete Workflow Command."""
from dataclasses import dataclass

from src.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteWorkflowCommand(Command):
    """Command to archive a workflow (soft delete)."""

    workflow_id: WorkflowId


class DeleteWorkflowCommandHandler(CommandHandler):
    """Handler for archiving a workflow."""

    def __init__(self, repository: WorkflowRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeleteWorkflowCommand) -> None:
        """
        Handle the delete workflow command by archiving the workflow.

        Args:
            command: The delete workflow command

        Raises:
            WorkflowNotFound: If workflow doesn't exist
        """
        # Get workflow
        workflow = self.repository.get_by_id(command.workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.workflow_id} not found")

        # Archive workflow (soft delete)
        workflow.archive()

        # Save changes
        self.repository.save(workflow)
