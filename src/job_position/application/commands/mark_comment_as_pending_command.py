"""Mark Job Position Comment As Pending Command."""
from dataclasses import dataclass

from src.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.job_position.domain.value_objects import JobPositionCommentId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class MarkJobPositionCommentAsPendingCommand(Command):
    """
    Command to mark a job position comment as pending
    """
    comment_id: str


class MarkJobPositionCommentAsPendingCommandHandler(CommandHandler[MarkJobPositionCommentAsPendingCommand]):
    """Handler for MarkJobPositionCommentAsPendingCommand"""

    def __init__(self, comment_repository: JobPositionCommentRepositoryInterface):
        self._repository = comment_repository

    def execute(self, command: MarkJobPositionCommentAsPendingCommand) -> None:
        """
        Execute the command

        Args:
            command: Command with ID of comment to mark as pending

        Raises:
            ValueError: If comment not found
        """
        # Retrieve the existing comment
        comment_id = JobPositionCommentId.from_string(command.comment_id)
        comment = self._repository.get_by_id(comment_id)

        if not comment:
            raise ValueError(f"Comment with ID {command.comment_id} not found")

        # Mark as pending
        comment.mark_as_pending()

        # Save the updated comment
        self._repository.save(comment)
