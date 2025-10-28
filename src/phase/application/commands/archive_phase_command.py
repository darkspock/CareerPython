"""Archive phase command"""
from dataclasses import dataclass

from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class ArchivePhaseCommand(Command):
    """Command to archive a phase (soft delete)"""
    phase_id: str


class ArchivePhaseCommandHandler(CommandHandler):
    """Handler for ArchivePhaseCommand"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def execute(self, command: ArchivePhaseCommand) -> None:
        """Execute the archive phase command"""
        phase_id = PhaseId.from_string(command.phase_id)

        phase = self.phase_repository.get_by_id(phase_id)
        if not phase:
            raise ValueError(f"Phase with id {command.phase_id} not found")

        phase.archive()
        self.phase_repository.save(phase)
