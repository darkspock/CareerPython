"""Update Job Position Comment Command."""
from dataclasses import dataclass
from typing import Optional

from src.job_position.domain.enums import CommentVisibilityEnum
from src.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.job_position.domain.value_objects import JobPositionCommentId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class UpdateJobPositionCommentCommand(Command):
    """
    Command to update a job position comment
    """
    comment_id: str
    comment: Optional[str] = None
    visibility: Optional[str] = None


class UpdateJobPositionCommentCommandHandler(CommandHandler[UpdateJobPositionCommentCommand]):
    """Handler for UpdateJobPositionCommentCommand"""

    def __init__(self, comment_repository: JobPositionCommentRepositoryInterface):
        self._repository = comment_repository

    def execute(self, command: UpdateJobPositionCommentCommand) -> None:
        """
        Execute the command

        Args:
            command: Command with data for updating the comment

        Raises:
            ValueError: If comment not found
        """
        # Retrieve the existing comment
        comment_id = JobPositionCommentId.from_string(command.comment_id)
        comment = self._repository.get_by_id(comment_id)

        if not comment:
            raise ValueError(f"Comment with ID {command.comment_id} not found")

        # Update the comment
        new_visibility = CommentVisibilityEnum(command.visibility) if command.visibility else None
        comment.update(
            comment=command.comment,
            visibility=new_visibility,
        )

        # Save the updated comment
        self._repository.save(comment)
