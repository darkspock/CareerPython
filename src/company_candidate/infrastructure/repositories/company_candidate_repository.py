from typing import Optional, List

from sqlalchemy.orm import Session

from src.company_candidate.domain.entities.company_candidate import CompanyCandidate
from src.company_candidate.domain.enums import (
    CompanyCandidateStatus,
    OwnershipStatus,
    CandidatePriority,
)
from src.company_candidate.domain.value_objects import (
    CompanyCandidateId,
    VisibilitySettings,
)
from src.company_candidate.domain.infrastructure.company_candidate_repository_interface import (
    CompanyCandidateRepositoryInterface
)
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from core.database import SQLAlchemyDatabase


class CompanyCandidateRepository(CompanyCandidateRepositoryInterface):
    """SQLAlchemy implementation of CompanyCandidateRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def _to_domain(self, model: CompanyCandidateModel) -> CompanyCandidate:
        """Convert model to domain entity"""
        return CompanyCandidate(
            id=CompanyCandidateId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            status=CompanyCandidateStatus(model.status),
            ownership_status=OwnershipStatus(model.ownership_status),
            created_by_user_id=CompanyUserId.from_string(model.created_by_user_id),
            workflow_id=model.workflow_id,
            current_stage_id=model.current_stage_id,
            invited_at=model.invited_at,
            confirmed_at=model.confirmed_at,
            rejected_at=model.rejected_at,
            archived_at=model.archived_at,
            visibility_settings=VisibilitySettings.from_dict(model.visibility_settings or {}),
            tags=model.tags or [],
            internal_notes=model.internal_notes or "",
            position=model.position,
            department=model.department,
            priority=CandidatePriority(model.priority),
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entity: CompanyCandidate) -> CompanyCandidateModel:
        """Convert domain entity to model"""
        return CompanyCandidateModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            candidate_id=str(entity.candidate_id),
            status=entity.status.value,
            ownership_status=entity.ownership_status.value,
            created_by_user_id=str(entity.created_by_user_id),
            workflow_id=entity.workflow_id,
            current_stage_id=entity.current_stage_id,
            invited_at=entity.invited_at,
            confirmed_at=entity.confirmed_at,
            rejected_at=entity.rejected_at,
            archived_at=entity.archived_at,
            visibility_settings=entity.visibility_settings.to_dict(),
            tags=entity.tags,
            internal_notes=entity.internal_notes,
            position=entity.position,
            department=entity.department,
            priority=entity.priority.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    def save(self, company_candidate: CompanyCandidate) -> None:
        """Save or update a company candidate relationship"""
        session = self._get_session()
        model = session.query(CompanyCandidateModel).filter_by(id=str(company_candidate.id)).first()

        if model:
            # Update existing
            model.company_id = str(company_candidate.company_id)
            model.candidate_id = str(company_candidate.candidate_id)
            model.status = company_candidate.status.value
            model.ownership_status = company_candidate.ownership_status.value
            model.created_by_user_id = str(company_candidate.created_by_user_id)
            model.workflow_id = company_candidate.workflow_id
            model.current_stage_id = company_candidate.current_stage_id
            model.invited_at = company_candidate.invited_at
            model.confirmed_at = company_candidate.confirmed_at
            model.rejected_at = company_candidate.rejected_at
            model.archived_at = company_candidate.archived_at
            model.visibility_settings = company_candidate.visibility_settings.to_dict()
            model.tags = company_candidate.tags
            model.internal_notes = company_candidate.internal_notes
            model.position = company_candidate.position
            model.department = company_candidate.department
            model.priority = company_candidate.priority.value
            model.updated_at = company_candidate.updated_at
        else:
            # Create new
            model = self._to_model(company_candidate)
            session.add(model)

        session.commit()

    def get_by_id(self, company_candidate_id: CompanyCandidateId) -> Optional[CompanyCandidate]:
        """Get a company candidate by ID"""
        session = self._get_session()
        model = session.query(CompanyCandidateModel).filter_by(id=str(company_candidate_id)).first()
        return self._to_domain(model) if model else None

    def get_by_company_and_candidate(
        self,
        company_id: CompanyId,
        candidate_id: CandidateId
    ) -> Optional[CompanyCandidate]:
        """Get a company candidate by company and candidate IDs"""
        session = self._get_session()
        model = session.query(CompanyCandidateModel).filter_by(
            company_id=str(company_id),
            candidate_id=str(candidate_id)
        ).first()
        return self._to_domain(model) if model else None

    def list_by_company(self, company_id: CompanyId) -> List[CompanyCandidate]:
        """List all company candidates for a company"""
        session = self._get_session()
        models = session.query(CompanyCandidateModel).filter_by(
            company_id=str(company_id)
        ).all()
        return [self._to_domain(model) for model in models]

    def list_by_candidate(self, candidate_id: CandidateId) -> List[CompanyCandidate]:
        """List all company candidates for a candidate"""
        session = self._get_session()
        models = session.query(CompanyCandidateModel).filter_by(
            candidate_id=str(candidate_id)
        ).all()
        return [self._to_domain(model) for model in models]

    def list_active_by_company(self, company_id: CompanyId) -> List[CompanyCandidate]:
        """List all active company candidates for a company"""
        session = self._get_session()
        models = session.query(CompanyCandidateModel).filter_by(
            company_id=str(company_id),
            status=CompanyCandidateStatus.ACTIVE.value
        ).all()
        return [self._to_domain(model) for model in models]

    def delete(self, company_candidate_id: CompanyCandidateId) -> None:
        """Delete a company candidate relationship"""
        session = self._get_session()
        session.query(CompanyCandidateModel).filter_by(id=str(company_candidate_id)).delete()
        session.commit()
