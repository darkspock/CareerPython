"""
Talent Pool Entry Repository Implementation
Phase 8: SQLAlchemy repository for talent pool entries
"""

from typing import List, Optional

from sqlalchemy import and_, or_, func
from sqlalchemy.orm import Session

from src.company_bc.talent_pool.domain.entities.talent_pool_entry import TalentPoolEntry
from src.company_bc.talent_pool.domain.enums.talent_pool_status import TalentPoolStatus
from src.company_bc.talent_pool.domain.infrastructure.talent_pool_entry_repository_interface import (
    TalentPoolEntryRepositoryInterface,
)
from src.company_bc.talent_pool.domain.value_objects.talent_pool_entry_id import TalentPoolEntryId
from src.company_bc.talent_pool.infrastructure.models.talent_pool_entry_model import TalentPoolEntryModel


class TalentPoolEntryRepository(TalentPoolEntryRepositoryInterface):
    """SQLAlchemy implementation of talent pool entry repository"""

    def __init__(self, database: Session):
        """
        Initialize repository.

        Args:
            database: SQLAlchemy session
        """
        self._db = database

    def get_by_id(self, entry_id: TalentPoolEntryId) -> Optional[TalentPoolEntry]:
        """Get a talent pool entry by ID"""
        model = self._db.query(TalentPoolEntryModel).filter(
            TalentPoolEntryModel.id == str(entry_id)
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def get_by_candidate(self, company_id: str, candidate_id: str) -> Optional[TalentPoolEntry]:
        """Get a talent pool entry for a specific candidate in a company"""
        model = self._db.query(TalentPoolEntryModel).filter(
            and_(
                TalentPoolEntryModel.company_id == company_id,
                TalentPoolEntryModel.candidate_id == candidate_id
            )
        ).first()

        if not model:
            return None

        return self._to_domain(model)

    def list_by_company(
            self,
            company_id: str,
            status: Optional[TalentPoolStatus] = None,
            tags: Optional[List[str]] = None,
            min_rating: Optional[int] = None,
    ) -> List[TalentPoolEntry]:
        """List talent pool entries for a company with optional filters"""
        query = self._db.query(TalentPoolEntryModel).filter(
            TalentPoolEntryModel.company_id == company_id
        )

        # Apply status filter
        if status:
            query = query.filter(TalentPoolEntryModel.status == status.value)

        # Apply min rating filter
        if min_rating is not None:
            query = query.filter(TalentPoolEntryModel.rating >= min_rating)

        # Apply tags filter (entries must have ALL specified tags)
        if tags:
            for tag in tags:
                query = query.filter(
                    func.json_contains(TalentPoolEntryModel.tags, f'"{tag}"')
                )

        # Order by updated_at descending
        query = query.order_by(TalentPoolEntryModel.updated_at.desc())

        models = query.all()
        return [self._to_domain(model) for model in models]

    def search(
            self,
            company_id: str,
            search_term: Optional[str] = None,
            status: Optional[TalentPoolStatus] = None,
            tags: Optional[List[str]] = None,
            min_rating: Optional[int] = None,
    ) -> List[TalentPoolEntry]:
        """Search talent pool entries with filters"""
        query = self._db.query(TalentPoolEntryModel).filter(
            TalentPoolEntryModel.company_id == company_id
        )

        # Apply search term (search in notes and added_reason)
        if search_term:
            search_pattern = f"%{search_term}%"
            query = query.filter(
                or_(
                    TalentPoolEntryModel.notes.ilike(search_pattern),
                    TalentPoolEntryModel.added_reason.ilike(search_pattern)
                )
            )

        # Apply status filter
        if status:
            query = query.filter(TalentPoolEntryModel.status == status.value)

        # Apply min rating filter
        if min_rating is not None:
            query = query.filter(TalentPoolEntryModel.rating >= min_rating)

        # Apply tags filter
        if tags:
            for tag in tags:
                query = query.filter(
                    func.json_contains(TalentPoolEntryModel.tags, f'"{tag}"')
                )

        # Order by updated_at descending
        query = query.order_by(TalentPoolEntryModel.updated_at.desc())

        models = query.all()
        return [self._to_domain(model) for model in models]

    def save(self, entry: TalentPoolEntry) -> None:
        """Save a talent pool entry (create or update)"""
        existing = self._db.query(TalentPoolEntryModel).filter(
            TalentPoolEntryModel.id == str(entry.id)
        ).first()

        if existing:
            # Update existing
            self._update_model_from_entity(existing, entry)
        else:
            # Create new
            model = self._to_model(entry)
            self._db.add(model)

        self._db.commit()

    def delete(self, entry_id: TalentPoolEntryId) -> None:
        """Delete a talent pool entry"""
        self._db.query(TalentPoolEntryModel).filter(
            TalentPoolEntryModel.id == str(entry_id)
        ).delete()
        self._db.commit()

    def exists(self, company_id: str, candidate_id: str) -> bool:
        """Check if a candidate exists in company's talent pool"""
        count = self._db.query(TalentPoolEntryModel).filter(
            and_(
                TalentPoolEntryModel.company_id == company_id,
                TalentPoolEntryModel.candidate_id == candidate_id
            )
        ).count()
        return count > 0

    def count_by_company(self, company_id: str, status: Optional[TalentPoolStatus] = None) -> int:
        """Count talent pool entries for a company"""
        query = self._db.query(TalentPoolEntryModel).filter(
            TalentPoolEntryModel.company_id == company_id
        )

        if status:
            query = query.filter(TalentPoolEntryModel.status == status.value)

        return query.count()

    def _to_domain(self, model: TalentPoolEntryModel) -> TalentPoolEntry:
        """Convert model to domain entity"""
        # Assert required fields are not None
        assert model.id is not None, "Model id cannot be None"
        assert model.company_id is not None, "Model company_id cannot be None"
        assert model.candidate_id is not None, "Model candidate_id cannot be None"
        assert model.created_at is not None, "Model created_at cannot be None"
        assert model.updated_at is not None, "Model updated_at cannot be None"

        return TalentPoolEntry._from_repository(
            id=TalentPoolEntryId.from_string(model.id),
            company_id=model.company_id,
            candidate_id=model.candidate_id,
            source_application_id=model.source_application_id,
            source_position_id=model.source_position_id,
            added_reason=model.added_reason,
            tags=model.tags if model.tags else [],
            rating=model.rating,
            notes=model.notes,
            status=TalentPoolStatus(model.status),
            added_by_user_id=model.added_by_user_id,
            created_at=model.created_at,
            updated_at=model.updated_at,
        )

    def _to_model(self, entry: TalentPoolEntry) -> TalentPoolEntryModel:
        """Convert domain entity to model"""
        return TalentPoolEntryModel(
            id=str(entry.id),
            company_id=entry.company_id,
            candidate_id=entry.candidate_id,
            source_application_id=entry.source_application_id,
            source_position_id=entry.source_position_id,
            added_reason=entry.added_reason,
            tags=entry.tags,
            rating=entry.rating,
            notes=entry.notes,
            status=entry.status.value,
            added_by_user_id=entry.added_by_user_id,
            created_at=entry.created_at,
            updated_at=entry.updated_at,
        )

    def _update_model_from_entity(self, model: TalentPoolEntryModel, entry: TalentPoolEntry) -> None:
        """Update model fields from entity"""
        model.company_id = entry.company_id
        model.candidate_id = entry.candidate_id
        model.source_application_id = entry.source_application_id
        model.source_position_id = entry.source_position_id
        model.added_reason = entry.added_reason
        model.tags = entry.tags
        model.rating = entry.rating
        model.notes = entry.notes
        model.status = entry.status.value
        model.added_by_user_id = entry.added_by_user_id
        model.updated_at = entry.updated_at
