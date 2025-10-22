"""Unset As Default Workflow Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.unset_as_default_workflow_command import UnsetAsDefaultWorkflowCommand
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound


class UnsetAsDefaultWorkflowCommandHandler(CommandHandler[UnsetAsDefaultWorkflowCommand, None]):
    """Handler for unsetting a workflow as default."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self.repository = repository

    def handle(self, command: UnsetAsDefaultWorkflowCommand) -> None:
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
        unset_workflow = workflow.unset_as_default()

        # Save changes
        self.repository.save(unset_workflow)
