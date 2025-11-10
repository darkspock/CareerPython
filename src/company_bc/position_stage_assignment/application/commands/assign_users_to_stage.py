"""Assign users to stage command"""
from dataclasses import dataclass
from typing import List

from src.company_bc.position_stage_assignment.domain import (
    PositionStageAssignment,
    PositionStageAssignmentId,
    PositionStageAssignmentRepositoryInterface
)
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class AssignUsersToStageCommand(Command):
    """Command to assign users to a position-stage combination"""
    position_id: str
    stage_id: str
    user_ids: List[str]


class AssignUsersToStageCommandHandler(CommandHandler[AssignUsersToStageCommand]):
    """Handler for assigning users to stage"""

    def __init__(self, repository: PositionStageAssignmentRepositoryInterface):
        self.repository = repository

    def execute(self, command: AssignUsersToStageCommand) -> None:
        """Execute the command"""
        # Check if assignment already exists
        existing = self.repository.get_by_position_and_stage(
            command.position_id,
            command.stage_id
        )

        if existing:
            # Update existing assignment
            existing.replace_users(command.user_ids)
            self.repository.save(existing)
        else:
            # Create new assignment
            assignment = PositionStageAssignment.create(
                id=PositionStageAssignmentId.generate(),
                position_id=command.position_id,
                stage_id=command.stage_id,
                assigned_user_ids=command.user_ids
            )
            self.repository.save(assignment)
