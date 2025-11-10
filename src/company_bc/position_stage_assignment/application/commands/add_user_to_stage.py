"""Add user to stage command"""
from dataclasses import dataclass

from src.company_bc.position_stage_assignment.domain import (
    PositionStageAssignment,
    PositionStageAssignmentId,
    PositionStageAssignmentRepositoryInterface
)
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class AddUserToStageCommand(Command):
    """Command to add a single user to a position-stage combination"""
    position_id: str
    stage_id: str
    user_id: str


class AddUserToStageCommandHandler(CommandHandler[AddUserToStageCommand]):
    """Handler for adding a user to stage"""

    def __init__(self, repository: PositionStageAssignmentRepositoryInterface):
        self.repository = repository

    def execute(self, command: AddUserToStageCommand) -> None:
        """Execute the command"""
        # Get existing assignment
        assignment = self.repository.get_by_position_and_stage(
            command.position_id,
            command.stage_id
        )

        if not assignment:
            # Create new assignment with this user
            assignment = PositionStageAssignment.create(
                id=PositionStageAssignmentId.generate(),
                position_id=command.position_id,
                stage_id=command.stage_id,
                assigned_user_ids=[command.user_id]
            )
        else:
            # Add user to existing assignment
            assignment.add_user(command.user_id)

        self.repository.save(assignment)
