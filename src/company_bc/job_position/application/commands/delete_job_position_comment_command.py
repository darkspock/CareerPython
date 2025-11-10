"""Delete Job Position Comment Command."""
from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.job_position.domain.value_objects import JobPositionCommentId
from src.company_bc.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)


@dataclass(frozen=True)
class DeleteJobPositionCommentCommand(Command):
    """
    Command to delete a job position comment
    """
    comment_id: str


class DeleteJobPositionCommentCommandHandler(CommandHandler[DeleteJobPositionCommentCommand]):
    """Handler for DeleteJobPositionCommentCommand"""

    def __init__(self, comment_repository: JobPositionCommentRepositoryInterface):
        self._repository = comment_repository

    def execute(self, command: DeleteJobPositionCommentCommand) -> None:
        """
        Execute the command
        
        Args:
            command: Command with ID of comment to delete
        """
        # Delete the comment
        comment_id = JobPositionCommentId.from_string(command.comment_id)
        self._repository.delete(comment_id)

