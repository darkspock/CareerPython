"""Deactivate Workflow Command."""
from dataclasses import dataclass

from src.shared_bc.customization.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeactivateWorkflowCommand(Command):
    """Command to deactivate a workflow."""

    workflow_id: WorkflowId


class DeactivateWorkflowCommandHandler(CommandHandler[DeactivateWorkflowCommand]):
    """Handler for deactivating a workflow."""

    def __init__(self, repository: WorkflowRepositoryInterface):
        self.repository = repository

    def execute(self, command: DeactivateWorkflowCommand) -> None:
        """
        Handle the deactivate workflow command.

        Args:
            command: The deactivate workflow command

        Raises:
            WorkflowNotFound: If workflow doesn't exist
        """
        # Get workflow
        workflow = self.repository.get_by_id(command.workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.workflow_id} not found")

        # deactivate() modifies the instance directly (mutability)
        workflow.deactivate()

        # Save changes
        self.repository.save(workflow)
