"""Set As Default Workflow Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.set_as_default_workflow_command import SetAsDefaultWorkflowCommand
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound


class SetAsDefaultWorkflowCommandHandler(CommandHandler[SetAsDefaultWorkflowCommand, None]):
    """Handler for setting a workflow as default."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self.repository = repository

    def handle(self, command: SetAsDefaultWorkflowCommand) -> None:
        """
        Handle the set as default workflow command.

        Args:
            command: The set as default workflow command

        Raises:
            WorkflowNotFound: If workflow doesn't exist
        """
        # Get workflow
        workflow = self.repository.get_by_id(command.workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.workflow_id} not found")

        # Get current default workflow (if any) and unset it
        current_default = self.repository.get_default_by_company(command.company_id)
        if current_default and current_default.id.value != command.workflow_id:
            unset_workflow = current_default.unset_as_default()
            self.repository.save(unset_workflow)

        # Set new default workflow
        default_workflow = workflow.set_as_default()

        # Save changes
        self.repository.save(default_workflow)
