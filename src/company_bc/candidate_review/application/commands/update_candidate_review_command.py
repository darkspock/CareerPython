from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.company_bc.candidate_review.domain.enums.review_score_enum import ReviewScoreEnum
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface


@dataclass(frozen=True)
class UpdateCandidateReviewCommand(Command):
    """Command to update a candidate review"""
    review_id: CandidateReviewId
    score: Optional[ReviewScoreEnum] = None
    comment: Optional[str] = None


class UpdateCandidateReviewCommandHandler(CommandHandler[UpdateCandidateReviewCommand]):
    """Handler for updating candidate reviews"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def execute(self, command: UpdateCandidateReviewCommand) -> None:
        """Handle the update candidate review command"""
        review = self._repository.get_by_id(command.review_id)
        if not review:
            raise ValueError(f"Review with id {command.review_id} not found")

        review.update(
            score=command.score,
            comment=command.comment,
        )
        
        self._repository.update(review)

