from dataclasses import dataclass
from typing import Optional

from src.shared.application.command_bus import Command, CommandHandler
from src.candidate_review.domain.entities.candidate_review import CandidateReview
from src.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.candidate_review.domain.enums.review_status_enum import ReviewStatusEnum
from src.candidate_review.domain.enums.review_score_enum import ReviewScoreEnum
from src.candidate_review.domain.infrastructure.candidate_review_repository_interface import CandidateReviewRepositoryInterface
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class CreateCandidateReviewCommand(Command):
    """Command to create a new candidate review"""
    company_candidate_id: CompanyCandidateId
    score: ReviewScoreEnum
    created_by_user_id: CompanyUserId
    comment: Optional[str] = None
    workflow_id: Optional[WorkflowId] = None
    stage_id: Optional[WorkflowStageId] = None
    review_status: ReviewStatusEnum = ReviewStatusEnum.REVIEWED


class CreateCandidateReviewCommandHandler(CommandHandler[CreateCandidateReviewCommand]):
    """Handler for creating candidate reviews"""

    def __init__(self, repository: CandidateReviewRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateCandidateReviewCommand) -> None:
        """Handle the create candidate review command"""
        review_id = CandidateReviewId.generate()
        review = CandidateReview.create(
            id=review_id,
            company_candidate_id=command.company_candidate_id,
            score=command.score,
            created_by_user_id=command.created_by_user_id,
            comment=command.comment,
            workflow_id=command.workflow_id,
            stage_id=command.stage_id,
            review_status=command.review_status,
        )
        
        self._repository.create(review)

