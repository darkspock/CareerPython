from dataclasses import dataclass

from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import \
    CandidateCommentRepositoryInterface
from src.company_candidate.domain.value_objects import CandidateCommentId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass(frozen=True)
class DeleteCandidateCommentCommand(Command):
    """Command to delete a candidate comment"""
    id: str


class DeleteCandidateCommentCommandHandler(CommandHandler[DeleteCandidateCommentCommand]):
    """Handler for deleting candidate comments"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteCandidateCommentCommand) -> None:
        """Handle the delete candidate comment command"""
        self._repository.delete(CandidateCommentId.from_string(command.id))
