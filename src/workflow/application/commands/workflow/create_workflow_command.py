from dataclasses import dataclass
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.workflow.domain.entities.workflow import Workflow
from src.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class CreateWorkflowCommand(Command):
    """Command to create a new workflow"""
    id: WorkflowId
    company_id: CompanyId
    workflow_type: WorkflowTypeEnum
    name: str
    description: str
    display: WorkflowDisplayEnum = WorkflowDisplayEnum.KANBAN
    phase_id: Optional[PhaseId] = None  # Phase 12: Phase association
    is_default: bool = False


class CreateWorkflowCommandHandler(CommandHandler[CreateWorkflowCommand]):
    """Handler for creating a new workflow"""

    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateWorkflowCommand) -> None:
        """Handle the create workflow command"""
        workflow = Workflow.create(
            id=command.id,
            company_id=command.company_id,
            workflow_type=command.workflow_type,
            name=command.name,
            description=command.description,
            display=command.display,
            phase_id=command.phase_id,
            is_default=command.is_default
        )

        self._repository.save(workflow)
