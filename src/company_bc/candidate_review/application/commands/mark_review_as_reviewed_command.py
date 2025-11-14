from dataclasses import dataclass

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class MarkReviewAsReviewedCommand(Command):
    """Command to mark a candidate review as reviewed"""
    review_id: CandidateReviewId


class MarkReviewAsReviewedCommandHandler(CommandHandler[MarkReviewAsReviewedCommand]):
    """Handler for marking candidate reviews as reviewed"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def execute(self, command: MarkReviewAsReviewedCommand) -> None:
        """Handle the mark review as reviewed command"""
        review = self._repository.get_by_id(command.review_id)
        if not review:
            raise ValueError(f"Review with id {command.review_id} not found")

        review.mark_as_reviewed()
        self._repository.update(review)

