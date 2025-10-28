"""Phase repository implementation"""
from typing import List, Optional

from core.database import DatabaseInterface
from src.company.domain.value_objects.company_id import CompanyId
from src.phase.domain.entities.phase import Phase
from src.phase.domain.enums.phase_status_enum import PhaseStatus
from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.phase.infrastructure.models.phase_model import PhaseModel


class PhaseRepository(PhaseRepositoryInterface):
    """SQLAlchemy implementation of PhaseRepository"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, phase: Phase) -> None:
        """Save a phase"""
        with self.database.get_session() as session:
            model = session.query(PhaseModel).filter_by(id=phase.id.value).first()

            if model:
                # Update existing
                model.company_id = phase.company_id.value
                model.name = phase.name
                model.sort_order = phase.sort_order
                model.default_view = phase.default_view
                model.status = phase.status
                model.objective = phase.objective
                model.updated_at = phase.updated_at
            else:
                # Create new
                model = PhaseModel(
                    id=phase.id.value,
                    company_id=phase.company_id.value,
                    name=phase.name,
                    sort_order=phase.sort_order,
                    default_view=phase.default_view,
                    status=phase.status,
                    objective=phase.objective,
                    created_at=phase.created_at,
                    updated_at=phase.updated_at
                )
                session.add(model)

            session.commit()

    def get_by_id(self, phase_id: PhaseId) -> Optional[Phase]:
        """Get phase by ID"""
        with self.database.get_session() as session:
            model = session.query(PhaseModel).filter_by(id=phase_id.value).first()

            if not model:
                return None

            return self._to_domain(model)

    def list_by_company(self, company_id: CompanyId) -> List[Phase]:
        """List all active (non-archived) phases for a company, ordered by sort_order"""
        with self.database.get_session() as session:
            models = (
                session.query(PhaseModel)
                .filter_by(company_id=company_id.value)
                .filter(PhaseModel.status != PhaseStatus.ARCHIVED)  # Exclude archived phases
                .order_by(PhaseModel.sort_order)
                .all()
            )

            return [self._to_domain(model) for model in models]

    def delete(self, phase_id: PhaseId) -> None:
        """Delete a phase"""
        with self.database.get_session() as session:
            session.query(PhaseModel).filter_by(id=phase_id.value).delete()
            session.commit()

    def exists(self, phase_id: PhaseId) -> bool:
        """Check if phase exists"""
        with self.database.get_session() as session:
            return session.query(PhaseModel).filter_by(id=phase_id.value).first() is not None

    def _to_domain(self, model: PhaseModel) -> Phase:
        """Convert model to domain entity"""
        return Phase._from_repository(
            id=PhaseId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            name=model.name,
            sort_order=model.sort_order,
            default_view=model.default_view,
            status=model.status,
            objective=model.objective,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
