"""Deactivate Workflow Command."""
from dataclasses import dataclass
from src.shared.application.command_bus import Command, CommandHandler
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId


@dataclass(frozen=True)
class DeactivateWorkflowCommand(Command):
    """Command to deactivate a workflow."""

    workflow_id: CompanyWorkflowId


class DeactivateWorkflowCommandHandler(CommandHandler[DeactivateWorkflowCommand]):
    """Handler for deactivating a workflow."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
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

        # Deactivate workflow
        deactivated_workflow = workflow.deactivate()

        # Save changes
        self.repository.save(deactivated_workflow)