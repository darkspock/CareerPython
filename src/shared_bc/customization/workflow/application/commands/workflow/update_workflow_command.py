from dataclasses import dataclass
from typing import Optional

from src.shared_bc.customization.workflow.domain.exceptions.workflow_not_found import WorkflowNotFound
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateWorkflowCommand(Command):
    """Command to update workflow information"""
    id: WorkflowId
    name: str
    description: str
    display: Optional[WorkflowDisplayEnum] = None
    phase_id: Optional[PhaseId] = None  # Phase 12: Phase association


class UpdateWorkflowCommandHandler(CommandHandler[UpdateWorkflowCommand]):
    """Handler for updating workflow information"""

    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateWorkflowCommand) -> None:
        """Handle the update workflow command"""
        workflow = self._repository.get_by_id(command.id)

        if not workflow:
            raise WorkflowNotFound(f"Workflow with id {command.id} not found")

        workflow.update(
            name=command.name,
            description=command.description,
            display=command.display,
            phase_id=command.phase_id
        )

        self._repository.save(workflow)
