from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.domain.entities.workflow import Workflow
from src.shared_bc.customization.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


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
