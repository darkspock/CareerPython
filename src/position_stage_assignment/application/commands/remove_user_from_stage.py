"""Remove user from stage command"""
from dataclasses import dataclass

from src.position_stage_assignment.domain import (
    PositionStageAssignmentRepositoryInterface,
    PositionStageAssignmentNotFoundException
)
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class RemoveUserFromStageCommand(Command):
    """Command to remove a user from a position-stage combination"""
    position_id: str
    stage_id: str
    user_id: str


class RemoveUserFromStageCommandHandler(CommandHandler[RemoveUserFromStageCommand]):
    """Handler for removing a user from stage"""

    def __init__(self, repository: PositionStageAssignmentRepositoryInterface):
        self.repository = repository

    def execute(self, command: RemoveUserFromStageCommand) -> None:
        """Execute the command"""
        # Get existing assignment
        assignment = self.repository.get_by_position_and_stage(
            command.position_id,
            command.stage_id
        )

        if not assignment:
            raise PositionStageAssignmentNotFoundException(
                f"No assignment found for position {command.position_id} and stage {command.stage_id}"
            )

        # Remove user
        assignment.remove_user(command.user_id)
        self.repository.save(assignment)
