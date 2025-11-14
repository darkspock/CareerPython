"""Mark Job Position Comment As Reviewed Command."""
from dataclasses import dataclass

from src.company_bc.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects import JobPositionCommentId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class MarkJobPositionCommentAsReviewedCommand(Command):
    """
    Command to mark a job position comment as reviewed
    """
    comment_id: str


class MarkJobPositionCommentAsReviewedCommandHandler(CommandHandler[MarkJobPositionCommentAsReviewedCommand]):
    """Handler for MarkCommentAsReviewedCommand"""

    def __init__(self, comment_repository: JobPositionCommentRepositoryInterface):
        self._repository = comment_repository

    def execute(self, command: MarkJobPositionCommentAsReviewedCommand) -> None:
        """
        Execute the command
        
        Args:
            command: Command with ID of comment to mark as reviewed
            
        Raises:
            ValueError: If comment not found
        """
        # Retrieve the existing comment
        comment_id = JobPositionCommentId.from_string(command.comment_id)
        comment = self._repository.get_by_id(comment_id)

        if not comment:
            raise ValueError(f"Comment with ID {command.comment_id} not found")

        # Mark as reviewed
        comment.mark_as_reviewed()

        # Save the updated comment
        self._repository.save(comment)
