"""Unset As Default Workflow Command."""
from dataclasses import dataclass

from src.shared_bc.customization.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UnsetAsDefaultWorkflowCommand(Command):
    """Command to unset a workflow as default."""

    workflow_id: WorkflowId


class UnsetAsDefaultWorkflowCommandHandler(CommandHandler[UnsetAsDefaultWorkflowCommand]):
    """Handler for unsetting a workflow as default."""

    def __init__(self, repository: WorkflowRepositoryInterface):
        self.repository = repository

    def execute(self, command: UnsetAsDefaultWorkflowCommand) -> None:
        """
        Handle the unset as default workflow command.

        Args:
            command: The unset as default workflow command

        Raises:
            WorkflowNotFound: If workflow doesn't exist
        """
        # Get workflow
        workflow = self.repository.get_by_id(command.workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.workflow_id} not found")

        # Unset as default
        workflow.unset_as_default()

        # Save changes
        self.repository.save(workflow)
