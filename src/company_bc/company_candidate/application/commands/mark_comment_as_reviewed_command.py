from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.value_objects import CandidateCommentId
from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import CandidateCommentRepositoryInterface


@dataclass(frozen=True)
class MarkCandidateCommentAsReviewedCommand(Command):
    """Command to mark a candidate comment as reviewed"""
    id: str


class MarkCandidateCommentAsReviewedCommandHandler(CommandHandler[MarkCandidateCommentAsReviewedCommand]):
    """Handler for marking candidate comments as reviewed"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def execute(self, command: MarkCandidateCommentAsReviewedCommand) -> None:
        """Handle the mark comment as reviewed command"""
        comment = self._repository.get_by_id(CandidateCommentId.from_string(command.id))
        if not comment:
            raise ValueError(f"Comment with id {command.id} not found")

        updated_comment = comment.mark_as_reviewed()
        self._repository.save(updated_comment)

