"""Update phase command"""
from dataclasses import dataclass

from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class UpdatePhaseCommand(Command):
    """Command to update an existing phase"""
    phase_id: PhaseId
    name: str
    sort_order: int
    default_view: DefaultView
    objective: str | None = None


class UpdatePhaseCommandHandler(CommandHandler[UpdatePhaseCommand]):
    """Handler for UpdatePhaseCommand"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def execute(self, command: UpdatePhaseCommand) -> None:
        """Execute the command to update a phase"""
        phase = self.phase_repository.get_by_id(command.phase_id)

        if not phase:
            raise ValueError(f"Phase with id {command.phase_id} not found")

        phase.update_details(
            name=command.name,
            sort_order=command.sort_order,
            default_view=command.default_view,
            objective=command.objective
        )

        self.phase_repository.save(phase)
