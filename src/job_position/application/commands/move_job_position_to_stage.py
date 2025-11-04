from dataclasses import dataclass
from typing import Optional

from src.shared.application.command_bus import Command, CommandHandler
from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.job_position.domain.value_objects.stage_id import StageId
from src.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface


@dataclass
class MoveJobPositionToStageCommand(Command):
    """Command to move a job position to a new stage"""
    id: JobPositionId
    stage_id: StageId
    comment: Optional[str] = None  # Optional comment for the stage change


class MoveJobPositionToStageCommandHandler(CommandHandler[MoveJobPositionToStageCommand]):
    """Handler for moving a job position to a new stage"""

    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: MoveJobPositionToStageCommand) -> None:
        """Execute the command - moves job position to new stage"""
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        # Move to new stage
        job_position.move_to_stage(command.stage_id)

        # TODO: In Phase 3, we'll also create a record in JobPositionStageHistory
        # This will be done when we implement the history system

        self.job_position_repository.save(job_position)

