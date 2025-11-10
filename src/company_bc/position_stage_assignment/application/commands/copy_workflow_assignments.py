"""Copy workflow assignments command"""
from dataclasses import dataclass
from typing import List

from src.company_bc.position_stage_assignment.domain import (
    PositionStageAssignment,
    PositionStageAssignmentId,
    PositionStageAssignmentRepositoryInterface
)
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class WorkflowStageAssignment:
    """DTO for workflow stage default assignments"""
    stage_id: str
    default_user_ids: List[str]


@dataclass
class CopyWorkflowAssignmentsCommand(Command):
    """Command to copy default assignments from workflow to position"""
    position_id: str
    workflow_stages: List[WorkflowStageAssignment]


class CopyWorkflowAssignmentsCommandHandler(CommandHandler[CopyWorkflowAssignmentsCommand]):
    """Handler for copying workflow assignments to position"""

    def __init__(self, repository: PositionStageAssignmentRepositoryInterface):
        self.repository = repository

    def execute(self, command: CopyWorkflowAssignmentsCommand) -> None:
        """Execute the command"""
        for stage_assignment in command.workflow_stages:
            # Skip if no default users
            if not stage_assignment.default_user_ids:
                continue

            # Check if assignment already exists
            existing = self.repository.get_by_position_and_stage(
                command.position_id,
                stage_assignment.stage_id
            )

            if existing:
                # Update existing assignment
                existing.replace_users(stage_assignment.default_user_ids)
                self.repository.save(existing)
            else:
                # Create new assignment
                assignment = PositionStageAssignment.create(
                    id=PositionStageAssignmentId.generate(),
                    position_id=command.position_id,
                    stage_id=stage_assignment.stage_id,
                    assigned_user_ids=stage_assignment.default_user_ids
                )
                self.repository.save(assignment)
