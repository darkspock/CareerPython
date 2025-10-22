from dataclasses import dataclass
from src.shared.application.command import Command, CommandHandler
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.exceptions.workflow_not_found import WorkflowNotFound

@dataclass(frozen=True)
class ActivateWorkflowCommand(Command):
    """Command to activate a workflow"""
    id: str


class ActivateWorkflowCommandHandler(CommandHandler[ActivateWorkflowCommand, None]):
    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, command: ActivateWorkflowCommand) -> None:
        workflow_id = CompanyWorkflowId.from_string(command.id)
        workflow = self._repository.get_by_id(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.id} not found")
        self._repository.save(workflow.activate())