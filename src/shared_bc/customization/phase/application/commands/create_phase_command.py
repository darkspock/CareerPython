"""Create phase command"""
from dataclasses import dataclass

from src.company_bc.company.domain.value_objects import CompanyId
from src.shared_bc.customization.phase.domain.entities.phase import Phase
from src.shared_bc.customization.phase.domain.enums.default_view_enum import DefaultView
from src.shared_bc.customization.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum


@dataclass
class CreatePhaseCommand(Command):
    """Command to create a new phase"""
    company_id: CompanyId
    workflow_type: WorkflowTypeEnum
    name: str
    sort_order: int
    default_view: DefaultView
    objective: str | None = None


class CreatePhaseCommandHandler(CommandHandler[CreatePhaseCommand]):
    """Handler for CreatePhaseCommand"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def execute(self, command: CreatePhaseCommand) -> None:
        """Execute the command to create a new phase"""
        phase_id = PhaseId.generate()

        phase = Phase.create(
            id=phase_id,
            workflow_type=command.workflow_type,
            company_id=command.company_id,
            name=command.name,
            sort_order=command.sort_order,
            default_view=command.default_view,
            objective=command.objective
        )

        self.phase_repository.save(phase)
