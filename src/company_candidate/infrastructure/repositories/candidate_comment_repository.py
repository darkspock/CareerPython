from typing import Optional, List

from sqlalchemy.orm import Session

from src.company_candidate.domain.entities.candidate_comment import CandidateComment
from src.company_candidate.domain.enums import (
    CommentVisibility,
    CommentReviewStatus,
)
from src.company_candidate.domain.value_objects import (
    CandidateCommentId,
    CompanyCandidateId,
)
from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import (
    CandidateCommentRepositoryInterface
)
from src.company_candidate.infrastructure.models.candidate_comment_model import CandidateCommentModel
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from core.database import SQLAlchemyDatabase


class CandidateCommentRepository(CandidateCommentRepositoryInterface):
    """SQLAlchemy implementation of CandidateCommentRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def _to_domain(self, model: CandidateCommentModel) -> CandidateComment:
        """Convert model to domain entity"""
        return CandidateComment(
            id=CandidateCommentId.from_string(model.id),
            company_candidate_id=CompanyCandidateId.from_string(model.company_candidate_id),
            comment=model.comment,
            workflow_id=CompanyWorkflowId.from_string(model.workflow_id) if model.workflow_id else None,
            stage_id=WorkflowStageId.from_string(model.stage_id) if model.stage_id else None,
            created_by_user_id=CompanyUserId.from_string(model.created_by_user_id),
            review_status=CommentReviewStatus(model.review_status),
            visibility=CommentVisibility(model.visibility),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: CandidateComment) -> CandidateCommentModel:
        """Convert domain entity to model"""
        return CandidateCommentModel(
            id=str(entity.id),
            company_candidate_id=str(entity.company_candidate_id),
            comment=entity.comment,
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            stage_id=str(entity.stage_id) if entity.stage_id else None,
            created_by_user_id=str(entity.created_by_user_id),
            review_status=entity.review_status.value,
            visibility=entity.visibility.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def save(self, comment: CandidateComment) -> None:
        """Save or update a comment"""
        session = self._get_session()
        model = self._to_model(comment)
        session.merge(model)
        session.commit()

    def get_by_id(self, comment_id: CandidateCommentId) -> Optional[CandidateComment]:
        """Get a comment by ID"""
        session = self._get_session()
        model = session.query(CandidateCommentModel).filter(
            CandidateCommentModel.id == str(comment_id)
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def list_by_company_candidate(
        self,
        company_candidate_id: CompanyCandidateId
    ) -> List[CandidateComment]:
        """List all comments for a company candidate"""
        session = self._get_session()
        models = session.query(CandidateCommentModel).filter(
            CandidateCommentModel.company_candidate_id == str(company_candidate_id)
        ).order_by(CandidateCommentModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def list_by_stage(
        self,
        company_candidate_id: CompanyCandidateId,
        stage_id: WorkflowStageId
    ) -> List[CandidateComment]:
        """List all comments for a company candidate in a specific stage"""
        session = self._get_session()
        models = session.query(CandidateCommentModel).filter(
            CandidateCommentModel.company_candidate_id == str(company_candidate_id),
            CandidateCommentModel.stage_id == str(stage_id)
        ).order_by(CandidateCommentModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def delete(self, comment_id: CandidateCommentId) -> None:
        """Delete a comment"""
        session = self._get_session()
        session.query(CandidateCommentModel).filter(
            CandidateCommentModel.id == str(comment_id)
        ).delete()
        session.commit()

    def count_pending_by_company_candidate(
        self,
        company_candidate_id: CompanyCandidateId
    ) -> int:
        """Count pending comments for a company candidate"""
        session = self._get_session()
        count = session.query(CandidateCommentModel).filter(
            CandidateCommentModel.company_candidate_id == str(company_candidate_id),
            CandidateCommentModel.review_status == CommentReviewStatus.PENDING.value
        ).count()

        return count

