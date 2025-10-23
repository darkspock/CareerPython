"""Set As Default Workflow Command."""
from dataclasses import dataclass
from src.shared.application.command_bus import Command, CommandHandler
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound


@dataclass(frozen=True)
class SetAsDefaultWorkflowCommand(Command):
    """Command to set a workflow as default for a company."""

    workflow_id: str
    company_id: str


class SetAsDefaultWorkflowCommandHandler(CommandHandler[SetAsDefaultWorkflowCommand]):
    """Handler for setting a workflow as default."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self.repository = repository

    def execute(self, command: SetAsDefaultWorkflowCommand) -> None:
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