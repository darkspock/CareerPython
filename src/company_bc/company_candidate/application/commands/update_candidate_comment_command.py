from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.value_objects import CandidateCommentId
from src.company_candidate.domain.enums import CommentVisibility
from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import CandidateCommentRepositoryInterface


@dataclass(frozen=True)
class UpdateCandidateCommentCommand(Command):
    """Command to update a candidate comment"""
    id: str
    comment: Optional[str] = None
    visibility: Optional[str] = None


class UpdateCandidateCommentCommandHandler(CommandHandler[UpdateCandidateCommentCommand]):
    """Handler for updating candidate comments"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateCandidateCommentCommand) -> None:
        """Handle the update candidate comment command"""
        existing_comment = self._repository.get_by_id(CandidateCommentId.from_string(command.id))
        if not existing_comment:
            raise ValueError(f"Comment with id {command.id} not found")

        visibility = CommentVisibility(command.visibility) if command.visibility else None
        updated_comment = existing_comment.update(
            comment=command.comment,
            visibility=visibility,
        )
        
        self._repository.save(updated_comment)

