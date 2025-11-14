from dataclasses import dataclass

from src.company_bc.company_candidate.domain.infrastructure.candidate_comment_repository_interface import \
    CandidateCommentRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects import CandidateCommentId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class MarkCommentAsPendingCommand(Command):
    """Command to mark a comment as pending review"""
    id: str


class MarkCommentAsPendingCommandHandler(CommandHandler[MarkCommentAsPendingCommand]):
    """Handler for marking comments as pending"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def execute(self, command: MarkCommentAsPendingCommand) -> None:
        """Handle the mark comment as pending command"""
        comment = self._repository.get_by_id(CandidateCommentId.from_string(command.id))
        if not comment:
            raise ValueError(f"Comment with id {command.id} not found")

        updated_comment = comment.mark_as_pending()
        self._repository.save(updated_comment)
