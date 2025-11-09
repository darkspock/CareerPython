"""Candidate Review Entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.candidate_review.domain.enums.review_status_enum import ReviewStatusEnum
from src.candidate_review.domain.enums.review_score_enum import ReviewScoreEnum
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass
class CandidateReview:
    """
    CandidateReview domain entity
    Represents a review with score for a candidate
    
    Reviews can be:
    - Global: visible at all stages (stage_id = None)
    - Stage-specific: only visible when candidate is in that stage (stage_id != None)
    """
    id: CandidateReviewId
    company_candidate_id: CompanyCandidateId
    score: ReviewScoreEnum
    comment: Optional[str]
    workflow_id: Optional[WorkflowId]
    stage_id: Optional[WorkflowStageId]
    review_status: ReviewStatusEnum
    created_by_user_id: CompanyUserId
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: CandidateReviewId,
        company_candidate_id: CompanyCandidateId,
        score: ReviewScoreEnum,
        created_by_user_id: CompanyUserId,
        comment: Optional[str] = None,
        workflow_id: Optional[WorkflowId] = None,
        stage_id: Optional[WorkflowStageId] = None,
        review_status: ReviewStatusEnum = ReviewStatusEnum.REVIEWED,
    ) -> "CandidateReview":
        """
        Factory method to create a new review

        Args:
            id: CandidateReview ID (required, must be provided from outside)
            company_candidate_id: CompanyCandidate ID this review belongs to
            score: Review score (0, 3, 6, 10)
            created_by_user_id: User who created this review
            comment: Optional comment text
            workflow_id: Optional workflow ID where review was made
            stage_id: Optional stage ID where review was made (None = global review)
            review_status: Review status (default: REVIEWED)

        Returns:
            CandidateReview: New review instance
            
        Raises:
            ValueError: If score is invalid
        """
        if score not in [ReviewScoreEnum.ZERO, ReviewScoreEnum.THREE, ReviewScoreEnum.SIX, ReviewScoreEnum.TEN]:
            raise ValueError("Score must be 0, 3, 6, or 10")

        now = datetime.utcnow()

        return cls(
            id=id,
            company_candidate_id=company_candidate_id,
            score=score,
            comment=comment.strip() if comment else None,
            workflow_id=workflow_id,
            stage_id=stage_id,
            review_status=review_status,
            created_by_user_id=created_by_user_id,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        score: Optional[ReviewScoreEnum] = None,
        comment: Optional[str] = None,
    ) -> None:
        """
        Update review score or comment

        Args:
            score: New review score (optional)
            comment: New comment text (optional, can be empty to clear)
            
        Raises:
            ValueError: If new score is invalid
        """
        if score is not None:
            if score not in [ReviewScoreEnum.ZERO, ReviewScoreEnum.THREE, ReviewScoreEnum.SIX, ReviewScoreEnum.TEN]:
                raise ValueError("Score must be 0, 3, 6, or 10")
            self.score = score

        if comment is not None:
            self.comment = comment.strip() if comment.strip() else None

        self.updated_at = datetime.utcnow()

    def mark_as_reviewed(self) -> None:
        """Mark this review as reviewed"""
        self.review_status = ReviewStatusEnum.REVIEWED
        self.updated_at = datetime.utcnow()

    def mark_as_pending(self) -> None:
        """Mark this review as pending review"""
        self.review_status = ReviewStatusEnum.PENDING
        self.updated_at = datetime.utcnow()

    @property
    def is_global(self) -> bool:
        """
        Check if this is a global review (visible at all stages)
        
        Returns:
            bool: True if stage_id is None (global review), False otherwise
        """
        return self.stage_id is None

