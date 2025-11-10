from typing import List, Optional

from core.database import DatabaseInterface
from src.candidate_bc.candidate.domain.entities import CandidateEducation
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.infrastructure.models import CandidateEducationModel
from src.framework.infrastructure.repositories.base import BaseRepository


class SQLAlchemyCandidateEducationRepository(CandidateEducationRepositoryInterface):
    """Implementación de repositorio de educación de candidatos con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, CandidateEducationModel)

    def _to_domain(self, model: CandidateEducationModel) -> CandidateEducation:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        from datetime import datetime
        return CandidateEducation(
            id=CandidateEducationId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            degree=model.degree,
            institution=model.institution,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            created_at=model.created_at or datetime.now(),
            updated_at=model.updated_at or datetime.now()
        )

    def _to_model(self, domain: CandidateEducation) -> CandidateEducationModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        model = CandidateEducationModel()
        # Set all fields manually to avoid constructor issues
        model.id = domain.id.value
        model.candidate_id = domain.candidate_id.value
        model.degree = domain.degree
        model.institution = domain.institution
        model.description = domain.description
        model.start_date = domain.start_date
        model.end_date = domain.end_date
        model.created_at = domain.created_at
        model.updated_at = domain.updated_at
        return model

    def create(self, candidate_education: CandidateEducation) -> CandidateEducation:
        model = self._to_model(candidate_education)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, candidate_education_id: CandidateEducationId) -> Optional[CandidateEducation]:
        model = self.base_repo.get_by_id(candidate_education_id)
        if model:
            return self._to_domain(model)
        return None

    def get_all(self, candidate_id: Optional[CandidateId] = None) -> List[CandidateEducation]:
        with self.database.get_session() as session:
            query = session.query(CandidateEducationModel)
            if candidate_id:
                query = query.filter(CandidateEducationModel.candidate_id == candidate_id.value)
            models = query.all()
            return [self._to_domain(model) for model in models]

    def get_by_candidate_id(self, id: CandidateId) -> List[CandidateEducation]:
        return self.get_all(candidate_id=id)

    def update(self, id: CandidateEducationId, candidate_education: CandidateEducation) -> None:
        with self.database.get_session() as session:
            model = session.query(CandidateEducationModel).filter(
                CandidateEducationModel.id == id.value).first()
            if model:
                model.degree = candidate_education.degree
                model.institution = candidate_education.institution
                model.description = candidate_education.description
                model.start_date = candidate_education.start_date
                model.end_date = candidate_education.end_date
                model.updated_at = candidate_education.updated_at
                session.commit()
            return

    def delete(self, id: CandidateEducationId) -> bool:
        return self.base_repo.delete(id)
