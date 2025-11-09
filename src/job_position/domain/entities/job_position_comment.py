"""Job Position Comment Entity."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.job_position.domain.value_objects import (
    JobPositionCommentId,
    JobPositionId,
    JobPositionWorkflowId,
    JobPositionStageId,
)
from src.job_position.domain.value_objects.workflow_stage import WorkflowStage
from src.job_position.domain.enums.comment_visibility import CommentVisibilityEnum
from src.job_position.domain.enums.comment_review_status import CommentReviewStatusEnum
from src.company.domain.value_objects.company_user_id import CompanyUserId


@dataclass
class JobPositionComment:
    """
    JobPositionComment domain entity
    Represents a comment on a job position
    
    Comments can be:
    - Global: visible at all stages (stage_id = None)
    - Stage-specific: only visible when position is in that stage (stage_id != None)
    """
    id: JobPositionCommentId
    job_position_id: JobPositionId
    comment: str
    workflow_id: Optional[JobPositionWorkflowId]
    stage_id: Optional[str]  # NULL = global comment (visible at all stages) - points to workflow_stages.id
    job_position_stage_id: Optional[JobPositionStageId]  # Points to job_position_stages.id (specific stage instance)
    created_by_user_id: CompanyUserId
    review_status: CommentReviewStatusEnum
    visibility: CommentVisibilityEnum
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: JobPositionCommentId,
        job_position_id: JobPositionId,
        comment: str,
        created_by_user_id: CompanyUserId,
        workflow_id: Optional[JobPositionWorkflowId] = None,
        stage_id: Optional[str] = None,
        job_position_stage_id: Optional[JobPositionStageId] = None,
        visibility: CommentVisibilityEnum = CommentVisibilityEnum.SHARED,
        review_status: CommentReviewStatusEnum = CommentReviewStatusEnum.REVIEWED,
    ) -> "JobPositionComment":
        """
        Factory method to create a new comment

        Args:
            id: JobPositionComment ID (required, must be provided from outside)
            job_position_id: JobPosition ID this comment belongs to
            comment: Comment text content
            created_by_user_id: User who created this comment
            workflow_id: Optional workflow ID where comment was made
            stage_id: Optional stage ID where comment was made (None = global comment) - points to workflow_stages.id
            job_position_stage_id: Optional job position stage ID (specific stage instance) - points to job_position_stages.id
            visibility: Visibility level of the comment
            review_status: Review status (default: REVIEWED)

        Returns:
            JobPositionComment: New comment instance
            
        Raises:
            ValueError: If comment text is empty
        """
        if not comment or not comment.strip():
            raise ValueError("Comment text cannot be empty")

        now = datetime.utcnow()

        return cls(
            id=id,
            job_position_id=job_position_id,
            comment=comment.strip(),
            workflow_id=workflow_id,
            stage_id=stage_id,
            job_position_stage_id=job_position_stage_id,
            created_by_user_id=created_by_user_id,
            review_status=review_status,
            visibility=visibility,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        comment: Optional[str] = None,
        visibility: Optional[CommentVisibilityEnum] = None,
    ) -> None:
        """
        Update comment content or visibility

        Args:
            comment: New comment text (optional)
            visibility: New visibility level (optional)
            
        Raises:
            ValueError: If new comment text is empty
        """
        if comment is not None:
            if not comment.strip():
                raise ValueError("Comment text cannot be empty")
            self.comment = comment.strip()

        if visibility is not None:
            self.visibility = visibility

        self.updated_at = datetime.utcnow()

    def mark_as_pending(self) -> None:
        """Mark this comment as pending review"""
        self.review_status = CommentReviewStatusEnum.PENDING
        self.updated_at = datetime.utcnow()

    def mark_as_reviewed(self) -> None:
        """Mark this comment as reviewed"""
        self.review_status = CommentReviewStatusEnum.REVIEWED
        self.updated_at = datetime.utcnow()

    @property
    def is_global(self) -> bool:
        """
        Check if this is a global comment (visible at all stages)
        
        Returns:
            bool: True if stage_id is None (global comment), False otherwise
        """
        return self.stage_id is None

