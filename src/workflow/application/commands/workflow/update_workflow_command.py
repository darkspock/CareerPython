from dataclasses import dataclass
from typing import Optional

from src.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateWorkflowCommand(Command):
    """Command to update workflow information"""
    id: str
    name: str
    description: str
    phase_id: Optional[str] = None  # Phase 12: Phase association


class UpdateWorkflowCommandHandler(CommandHandler[UpdateWorkflowCommand]):
    """Handler for updating workflow information"""

    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateWorkflowCommand) -> None:
        """Handle the update workflow command"""
        workflow_id = WorkflowId.from_string(command.id)
        workflow = self._repository.get_by_id(workflow_id)

        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.id} not found")

        workflow.update(
            name=command.name,
            description=command.description,
            phase_id=command.phase_id  # Phase 12: Phase association
        )

        self._repository.save(workflow)
