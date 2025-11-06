from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company_candidate.domain.value_objects import (
    CandidateCommentId,
    CompanyCandidateId,
)
from src.company_candidate.domain.enums import (
    CommentVisibility,
    CommentReviewStatus,
)
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass
class CandidateComment:
    """
    CandidateComment domain entity
    Represents a comment on a company candidate
    """
    id: CandidateCommentId
    company_candidate_id: CompanyCandidateId
    comment: str
    workflow_id: Optional[WorkflowId]
    stage_id: Optional[WorkflowStageId]
    created_by_user_id: CompanyUserId
    review_status: CommentReviewStatus
    visibility: CommentVisibility
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: CandidateCommentId,
        company_candidate_id: CompanyCandidateId,
        comment: str,
        created_by_user_id: CompanyUserId,
        workflow_id: Optional[WorkflowId] = None,
        stage_id: Optional[WorkflowStageId] = None,
        visibility: CommentVisibility = CommentVisibility.PRIVATE,
        review_status: CommentReviewStatus = CommentReviewStatus.REVIEWED,
    ) -> "CandidateComment":
        """
        Factory method to create a new comment

        Args:
            id: CandidateComment ID (required, must be provided from outside)
            company_candidate_id: CompanyCandidate ID this comment belongs to
            comment: Comment text content
            created_by_user_id: User who created this comment
            workflow_id: Optional workflow ID where comment was made
            stage_id: Optional stage ID where comment was made
            visibility: Visibility level of the comment
            review_status: Review status (default: REVIEWED)

        Returns:
            CandidateComment: New comment instance
        """
        if not comment or not comment.strip():
            raise ValueError("Comment text cannot be empty")

        now = datetime.utcnow()

        return cls(
            id=id,
            company_candidate_id=company_candidate_id,
            comment=comment.strip(),
            workflow_id=workflow_id,
            stage_id=stage_id,
            created_by_user_id=created_by_user_id,
            review_status=review_status,
            visibility=visibility,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        comment: Optional[str] = None,
        visibility: Optional[CommentVisibility] = None,
    ) -> "CandidateComment":
        """
        Update comment content or visibility

        Args:
            comment: New comment text (optional)
            visibility: New visibility level (optional)

        Returns:
            CandidateComment: New instance with updated fields
        """
        if comment is not None and not comment.strip():
            raise ValueError("Comment text cannot be empty")

        return CandidateComment(
            id=self.id,
            company_candidate_id=self.company_candidate_id,
            comment=comment.strip() if comment is not None else self.comment,
            workflow_id=self.workflow_id,
            stage_id=self.stage_id,
            created_by_user_id=self.created_by_user_id,
            review_status=self.review_status,
            visibility=visibility if visibility is not None else self.visibility,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def mark_as_pending(self) -> "CandidateComment":
        """
        Mark comment as pending review

        Returns:
            CandidateComment: New instance with PENDING review status
        """
        if self.review_status == CommentReviewStatus.PENDING:
            return self

        return CandidateComment(
            id=self.id,
            company_candidate_id=self.company_candidate_id,
            comment=self.comment,
            workflow_id=self.workflow_id,
            stage_id=self.stage_id,
            created_by_user_id=self.created_by_user_id,
            review_status=CommentReviewStatus.PENDING,
            visibility=self.visibility,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def mark_as_reviewed(self) -> "CandidateComment":
        """
        Mark comment as reviewed

        Returns:
            CandidateComment: New instance with REVIEWED review status
        """
        if self.review_status == CommentReviewStatus.REVIEWED:
            return self

        return CandidateComment(
            id=self.id,
            company_candidate_id=self.company_candidate_id,
            comment=self.comment,
            workflow_id=self.workflow_id,
            stage_id=self.stage_id,
            created_by_user_id=self.created_by_user_id,
            review_status=CommentReviewStatus.REVIEWED,
            visibility=self.visibility,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

