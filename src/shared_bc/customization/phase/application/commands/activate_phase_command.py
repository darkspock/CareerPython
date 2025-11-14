"""Activate phase command"""
from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


@dataclass
class ActivatePhaseCommand(Command):
    """Command to activate a phase"""
    phase_id: str


class ActivatePhaseCommandHandler(CommandHandler):
    """Handler for ActivatePhaseCommand"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def execute(self, command: ActivatePhaseCommand) -> None:
        """Execute the activate phase command"""
        phase_id = PhaseId.from_string(command.phase_id)

        phase = self.phase_repository.get_by_id(phase_id)
        if not phase:
            raise ValueError(f"Phase with id {command.phase_id} not found")

        phase.activate()
        self.phase_repository.save(phase)
