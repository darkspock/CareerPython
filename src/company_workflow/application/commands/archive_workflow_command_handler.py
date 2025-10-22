"""Archive Workflow Command Handler."""
from src.shared.application.command import CommandHandler
from src.company_workflow.application.commands.archive_workflow_command import ArchiveWorkflowCommand
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound


class ArchiveWorkflowCommandHandler(CommandHandler[ArchiveWorkflowCommand, None]):
    """Handler for archiving a workflow."""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self.repository = repository

    def handle(self, command: ArchiveWorkflowCommand) -> None:
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
