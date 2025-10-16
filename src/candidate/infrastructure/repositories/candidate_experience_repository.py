from typing import List, Optional, Dict, Any

from core.database import DatabaseInterface
from src.candidate.domain.entities import CandidateExperience
from src.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate.infrastructure.models import CandidateExperienceModel
from src.shared.infrastructure.repositories.base import BaseRepository


class SQLAlchemyCandidateExperienceRepository(CandidateExperienceRepositoryInterface):
    """Implementación de repositorio de experiencia laboral de candidatos con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, CandidateExperienceModel)

    def _to_domain(self, model: CandidateExperienceModel) -> CandidateExperience:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        from datetime import datetime
        return CandidateExperience(
            id=CandidateExperienceId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            job_title=model.job_title,
            company=model.company,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            created_at=model.created_at or datetime.now(),
            updated_at=model.updated_at or datetime.now()
        )

    def _to_model(self, domain: CandidateExperience) -> CandidateExperienceModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        model = CandidateExperienceModel()
        # Set all fields manually to avoid constructor issues
        model.id = domain.id.value
        model.candidate_id = domain.candidate_id.value
        model.job_title = domain.job_title
        model.company = domain.company
        model.description = domain.description
        model.start_date = domain.start_date
        model.end_date = domain.end_date
        model.created_at = domain.created_at
        model.updated_at = domain.updated_at
        return model

    def create(self, candidate_experience: CandidateExperience) -> CandidateExperience:
        model = self._to_model(candidate_experience)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, id: CandidateExperienceId) -> Optional[CandidateExperience]:
        model = self.base_repo.get_by_id(id)
        if model:
            return self._to_domain(model)
        return None

    def get_all(self, candidate_id: Optional[CandidateId] = None) -> List[CandidateExperience]:
        with self.database.get_session() as session:
            query = session.query(CandidateExperienceModel)
            if candidate_id:
                query = query.filter(CandidateExperienceModel.candidate_id == candidate_id.value)
            models = query.all()
            return [self._to_domain(model) for model in models]

    def get_by_candidate_id(self, id: CandidateId) -> List[CandidateExperience]:
        return self.get_all(candidate_id=id)

    def update(self, id: CandidateExperienceId, candidate_experience_data: Dict[str, Any]) -> Optional[
        CandidateExperience]:
        if not id:
            raise ValueError("candidate_experience_id must be provided")

        with self.database.get_session() as session:
            model = session.query(CandidateExperienceModel).filter(CandidateExperienceModel.id == id.value).first()
            if model:
                for key, value in candidate_experience_data.items():
                    if value is not None:
                        setattr(model, key, value)
                session.commit()
                session.refresh(model)
                return self._to_domain(model)
            return None

    def delete(self, id: CandidateExperienceId) -> bool:
        return self.base_repo.delete(id)
