from typing import Optional, List

from sqlalchemy.orm import Session

from src.company_bc.candidate_review.domain.entities.candidate_review import CandidateReview
from src.company_bc.candidate_review.domain.enums import (
    ReviewStatusEnum,
    ReviewScoreEnum,
)
from src.company_bc.candidate_review.domain.value_objects.candidate_review_id import CandidateReviewId
from src.company_bc.candidate_review.domain.infrastructure.candidate_review_repository_interface import (
    CandidateReviewRepositoryInterface
)
from src.company_bc.candidate_review.infrastructure.models.candidate_review_model import CandidateReviewModel
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from core.database import SQLAlchemyDatabase


class CandidateReviewRepository(CandidateReviewRepositoryInterface):
    """SQLAlchemy implementation of CandidateReviewRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def _to_domain(self, model: CandidateReviewModel) -> CandidateReview:
        """Convert model to domain entity"""
        return CandidateReview(
            id=CandidateReviewId.from_string(model.id),
            company_candidate_id=CompanyCandidateId.from_string(model.company_candidate_id),
            score=ReviewScoreEnum(model.score),
            comment=model.comment,
            workflow_id=WorkflowId.from_string(model.workflow_id) if model.workflow_id else None,
            stage_id=WorkflowStageId.from_string(model.stage_id) if model.stage_id else None,
            review_status=ReviewStatusEnum(model.review_status),
            created_by_user_id=CompanyUserId.from_string(model.created_by_user_id),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: CandidateReview) -> CandidateReviewModel:
        """Convert domain entity to model"""
        return CandidateReviewModel(
            id=str(entity.id),
            company_candidate_id=str(entity.company_candidate_id),
            score=entity.score.value,
            comment=entity.comment,
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            stage_id=str(entity.stage_id) if entity.stage_id else None,
            review_status=entity.review_status.value,
            created_by_user_id=str(entity.created_by_user_id),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def get_by_id(self, review_id: CandidateReviewId) -> Optional[CandidateReview]:
        """Get a review by ID"""
        session = self._get_session()
        model = session.query(CandidateReviewModel).filter(
            CandidateReviewModel.id == str(review_id)
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def get_by_company_candidate(
        self, 
        company_candidate_id: CompanyCandidateId
    ) -> List[CandidateReview]:
        """Get all reviews for a company candidate"""
        session = self._get_session()
        models = session.query(CandidateReviewModel).filter(
            CandidateReviewModel.company_candidate_id == str(company_candidate_id)
        ).order_by(CandidateReviewModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def get_by_stage(
        self, 
        company_candidate_id: CompanyCandidateId, 
        stage_id: WorkflowStageId
    ) -> List[CandidateReview]:
        """Get all reviews for a specific stage"""
        session = self._get_session()
        models = session.query(CandidateReviewModel).filter(
            CandidateReviewModel.company_candidate_id == str(company_candidate_id),
            CandidateReviewModel.stage_id == str(stage_id)
        ).order_by(CandidateReviewModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def get_global_reviews(
        self, 
        company_candidate_id: CompanyCandidateId
    ) -> List[CandidateReview]:
        """Get all global reviews (stage_id is None)"""
        session = self._get_session()
        models = session.query(CandidateReviewModel).filter(
            CandidateReviewModel.company_candidate_id == str(company_candidate_id),
            CandidateReviewModel.stage_id.is_(None)
        ).order_by(CandidateReviewModel.created_at.desc()).all()

        return [self._to_domain(model) for model in models]

    def create(self, review: CandidateReview) -> None:
        """Create a new review"""
        session = self._get_session()
        model = self._to_model(review)
        session.add(model)
        session.commit()

    def update(self, review: CandidateReview) -> None:
        """Update an existing review"""
        session = self._get_session()
        model = self._to_model(review)
        session.merge(model)
        session.commit()

    def delete(self, review_id: CandidateReviewId) -> None:
        """Delete a review"""
        session = self._get_session()
        model = session.query(CandidateReviewModel).filter(
            CandidateReviewModel.id == str(review_id)
        ).first()

        if model:
            session.delete(model)
            session.commit()

