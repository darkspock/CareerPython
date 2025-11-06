"""Job Position Comment Repository Implementation."""
from typing import Optional, List

from sqlalchemy import or_
from sqlalchemy.orm import Session

from core.database import SQLAlchemyDatabase
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.job_position.domain.entities.job_position_comment import JobPositionComment
from src.job_position.domain.enums import (
    CommentVisibilityEnum,
    CommentReviewStatusEnum,
)
from src.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.job_position.domain.value_objects import (
    JobPositionCommentId,
    JobPositionId,
    JobPositionWorkflowId,
)
from src.job_position.infrastructure.models.job_position_comment_model import JobPositionCommentModel


class JobPositionCommentRepository(JobPositionCommentRepositoryInterface):
    """SQLAlchemy implementation of JobPositionCommentRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def _to_domain(self, model: JobPositionCommentModel) -> JobPositionComment:
        """Convert model to domain entity"""
        return JobPositionComment(
            id=JobPositionCommentId.from_string(model.id),
            job_position_id=JobPositionId.from_string(model.job_position_id),
            comment=model.comment,
            workflow_id=JobPositionWorkflowId.from_string(model.workflow_id) if model.workflow_id else None,
            stage_id=model.stage_id,  # Keep as string (can be None for global comments)
            created_by_user_id=CompanyUserId.from_string(model.created_by_user_id),
            review_status=CommentReviewStatusEnum(model.review_status),
            visibility=CommentVisibilityEnum(model.visibility),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: JobPositionComment) -> JobPositionCommentModel:
        """Convert domain entity to model"""
        return JobPositionCommentModel(
            id=str(entity.id),
            job_position_id=str(entity.job_position_id),
            comment=entity.comment,
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            stage_id=entity.stage_id,  # Already a string (or None for global comments)
            created_by_user_id=str(entity.created_by_user_id),
            review_status=entity.review_status.value,
            visibility=entity.visibility.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def save(self, comment: JobPositionComment) -> None:
        """Save or update a comment"""
        session = self._get_session()
        model = self._to_model(comment)
        session.merge(model)
        session.commit()

    def get_by_id(self, comment_id: JobPositionCommentId) -> Optional[JobPositionComment]:
        """Get a comment by ID"""
        session = self._get_session()
        model = session.query(JobPositionCommentModel).filter(
            JobPositionCommentModel.id == str(comment_id)
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def list_by_job_position(
            self,
            job_position_id: JobPositionId,
            current_user_id: Optional[str] = None
    ) -> List[JobPositionComment]:
        """
        List all comments for a job position with visibility filtering.

        PRIVATE comments are only visible to their creator.
        SHARED comments are visible to all team members.
        """
        session = self._get_session()
        query = session.query(JobPositionCommentModel).filter(
            JobPositionCommentModel.job_position_id == str(job_position_id)
        )

        # Apply visibility filtering if current_user_id is provided
        if current_user_id:
            query = query.filter(
                or_(
                    # Show SHARED comments to everyone
                    JobPositionCommentModel.visibility == CommentVisibilityEnum.SHARED.value,
                    # Show PRIVATE comments only to their creator
                    (
                            (JobPositionCommentModel.visibility == CommentVisibilityEnum.PRIVATE.value) &
                            (JobPositionCommentModel.created_by_user_id == current_user_id)
                    )
                )
            )

        models = query.order_by(JobPositionCommentModel.created_at.desc()).all()
        return [self._to_domain(model) for model in models]

    def list_by_stage_and_global(
            self,
            job_position_id: JobPositionId,
            stage_id: Optional[str],
            include_global: bool = True,
            current_user_id: Optional[str] = None
    ) -> List[JobPositionComment]:
        """
        List comments for a job position, filtered by stage, and optionally including global comments.

        Visibility filtering:
        - PRIVATE comments: only visible to their creator
        - SHARED comments: visible to all team members

        Args:
            job_position_id: ID of the job position
            stage_id: ID of the stage (can be None to get only global comments)
            include_global: If True, includes global comments (stage_id IS NULL)
            current_user_id: ID of the current user (for filtering PRIVATE comments)

        Returns:
            List[JobPositionComment]: Filtered comments (ordered by created_at DESC)
        """
        session = self._get_session()

        # Build query: job_position_id matches
        query = session.query(JobPositionCommentModel).filter(
            JobPositionCommentModel.job_position_id == str(job_position_id)
        )

        # Stage filtering
        if stage_id is not None:
            # Filter for specific stage
            if include_global:
                # Include both stage-specific AND global comments
                query = query.filter(
                    or_(
                        JobPositionCommentModel.stage_id == stage_id,
                        JobPositionCommentModel.stage_id.is_(None)
                    )
                )
            else:
                # Only stage-specific comments
                query = query.filter(JobPositionCommentModel.stage_id == stage_id)
        else:
            # If stage_id is None, only get global comments
            query = query.filter(JobPositionCommentModel.stage_id.is_(None))

        # Visibility filtering
        if current_user_id:
            query = query.filter(
                or_(
                    # Show SHARED comments to everyone
                    JobPositionCommentModel.visibility == CommentVisibilityEnum.SHARED.value,
                    # Show PRIVATE comments only to their creator
                    (
                            (JobPositionCommentModel.visibility == CommentVisibilityEnum.PRIVATE.value) &
                            (JobPositionCommentModel.created_by_user_id == current_user_id)
                    )
                )
            )

        models = query.order_by(JobPositionCommentModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def list_global_only(
            self,
            job_position_id: JobPositionId
    ) -> List[JobPositionComment]:
        """List only global comments for a job position"""
        session = self._get_session()
        models = session.query(JobPositionCommentModel).filter(
            JobPositionCommentModel.job_position_id == str(job_position_id),
            JobPositionCommentModel.stage_id.is_(None)  # Only global comments (stage_id IS NULL)
        ).order_by(JobPositionCommentModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def delete(self, comment_id: JobPositionCommentId) -> None:
        """Delete a comment"""
        session = self._get_session()
        session.query(JobPositionCommentModel).filter(
            JobPositionCommentModel.id == str(comment_id)
        ).delete()
        session.commit()

    def count_pending_by_job_position(
            self,
            job_position_id: JobPositionId
    ) -> int:
        """Count pending comments for a job position"""
        session = self._get_session()
        count = session.query(JobPositionCommentModel).filter(
            JobPositionCommentModel.job_position_id == str(job_position_id),
            JobPositionCommentModel.review_status == CommentReviewStatusEnum.PENDING.value
        ).count()

        return count
