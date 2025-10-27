"""Create phase command"""
from dataclasses import dataclass

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.domain.entities.phase import Phase
from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId


@dataclass
class CreatePhaseCommand:
    """Command to create a new phase"""
    company_id: CompanyId
    name: str
    sort_order: int
    default_view: DefaultView
    objective: str | None = None


class CreatePhaseCommandHandler:
    """Handler for CreatePhaseCommand"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def execute(self, command: CreatePhaseCommand) -> None:
        """Execute the command to create a new phase"""
        phase_id = PhaseId.generate()

        phase = Phase.create(
            id=phase_id,
            company_id=command.company_id,
            name=command.name,
            sort_order=command.sort_order,
            default_view=command.default_view,
            objective=command.objective
        )

        self.phase_repository.save(phase)
