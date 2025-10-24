"""Archive Workflow Command."""
from dataclasses import dataclass

from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import \
    CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ArchiveWorkflowCommand(Command):
    """Command to archive a workflow."""

    workflow_id: CompanyWorkflowId


class ArchiveWorkflowCommandHandler(CommandHandler):
    """Handler for archiving a workflow."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self.repository = repository

    def execute(self, command: ArchiveWorkflowCommand) -> None:
        """
        Handle the archive workflow command.

        Args:
            command: The archive workflow command

        Raises:
            WorkflowNotFound: If workflow doesn't exist
        """
        # Get workflow
        workflow = self.repository.get_by_id(command.workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.workflow_id} not found")

        # Archive workflow
        archived_workflow = workflow.archive()

        # Save changes
        self.repository.save(archived_workflow)
