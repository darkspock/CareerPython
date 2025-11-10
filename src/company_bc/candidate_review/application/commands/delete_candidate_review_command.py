from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class DeleteCandidateReviewCommand(Command):
    """Command to delete a candidate review"""
    review_id: CandidateReviewId


class DeleteCandidateReviewCommandHandler(CommandHandler[DeleteCandidateReviewCommand]):
    """Handler for deleting candidate reviews"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def execute(self, command: DeleteCandidateReviewCommand) -> None:
        """Handle the delete candidate review command"""
        self._repository.delete(command.review_id)

