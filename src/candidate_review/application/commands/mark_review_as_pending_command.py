from dataclasses import dataclass

from src.shared.application.command_bus import Command, CommandHandler
from src.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class MarkReviewAsPendingCommand(Command):
    """Command to mark a candidate review as pending"""
    review_id: CandidateReviewId


class MarkReviewAsPendingCommandHandler(CommandHandler[MarkReviewAsPendingCommand]):
    """Handler for marking candidate reviews as pending"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def execute(self, command: MarkReviewAsPendingCommand) -> None:
        """Handle the mark review as pending command"""
        review = self._repository.get_by_id(command.review_id)
        if not review:
            raise ValueError(f"Review with id {command.review_id} not found")

        review.mark_as_pending()
        self._repository.update(review)

