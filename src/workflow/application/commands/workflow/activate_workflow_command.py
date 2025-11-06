from dataclasses import dataclass

from src.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class ActivateWorkflowCommand(Command):
    """Command to activate a workflow"""
    id: str


class ActivateWorkflowCommandHandler(CommandHandler[ActivateWorkflowCommand]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: ActivateWorkflowCommand) -> None:
        workflow_id = WorkflowId.from_string(command.id)
        workflow = self._repository.get_by_id(workflow_id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.id} not found")
        self._repository.save(workflow.activate())
