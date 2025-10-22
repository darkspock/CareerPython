from dataclasses import dataclass

from src.shared.application.command import Command, CommandHandler
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound


@dataclass(frozen=True)
class UpdateWorkflowCommand(Command):
    """Command to update workflow information"""
    id: str
    name: str
    description: str


class UpdateWorkflowCommandHandler(CommandHandler[UpdateWorkflowCommand, None]):
    """Handler for updating workflow information"""

    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, command: UpdateWorkflowCommand) -> None:
        """Handle the update workflow command"""
        workflow_id = CompanyWorkflowId.from_string(command.id)
        workflow = self._repository.get_by_id(workflow_id)

        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.id} not found")

        updated_workflow = workflow.update(
            name=command.name,
            description=command.description
        )

        self._repository.save(updated_workflow)