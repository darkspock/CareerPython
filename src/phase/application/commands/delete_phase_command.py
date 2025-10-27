"""Delete phase command"""
from dataclasses import dataclass

from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class DeletePhaseCommand(Command):
    """Command to delete a phase"""
    phase_id: PhaseId


class DeletePhaseCommandHandler(CommandHandler[DeletePhaseCommand]):
    """Handler for DeletePhaseCommand"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def execute(self, command: DeletePhaseCommand) -> None:
        """Execute the command to delete a phase

        Note: This should validate that no workflows are associated with this phase
        before deletion, but for now we'll do a simple delete
        """
        phase = self.phase_repository.get_by_id(command.phase_id)

        if not phase:
            raise ValueError(f"Phase with id {command.phase_id} not found")

        self.phase_repository.delete(command.phase_id)
