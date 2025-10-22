"""Deactivate Workflow Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.deactivate_workflow_command import DeactivateWorkflowCommand
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound


class DeactivateWorkflowCommandHandler(CommandHandler[DeactivateWorkflowCommand, None]):
    """Handler for deactivating a workflow."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self.repository = repository

    def handle(self, command: DeactivateWorkflowCommand) -> None:
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
