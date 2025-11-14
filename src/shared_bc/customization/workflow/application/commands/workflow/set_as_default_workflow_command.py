"""Set As Default Workflow Command."""
from dataclasses import dataclass

from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class SetAsDefaultWorkflowCommand(Command):
    """Command to set a workflow as default for a company."""

    workflow_id: WorkflowId
    company_id: CompanyId


class SetAsDefaultWorkflowCommandHandler(CommandHandler[SetAsDefaultWorkflowCommand]):
    """Handler for setting a workflow as default."""

    def __init__(self, repository: WorkflowRepositoryInterface):
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

        # Get current default workflow of the same type (if any) and unset it
        current_default = self.repository.get_default_by_company(command.company_id, workflow.workflow_type)
        if current_default and current_default.id != command.workflow_id:
            current_default.unset_as_default()
            self.repository.save(current_default)

        # Set new default workflow
        workflow.set_as_default()

        # Save changes
        self.repository.save(workflow)
