from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class ActivateWorkflowCommand(Command):
    """Command to activate a workflow"""
    id: WorkflowId


class ActivateWorkflowCommandHandler(CommandHandler[ActivateWorkflowCommand]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: ActivateWorkflowCommand) -> None:
        workflow = self._repository.get_by_id(command.id)
        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.id} not found")

        # activate() modifies the instance directly (mutability)
        workflow.activate()
        self._repository.save(workflow)
