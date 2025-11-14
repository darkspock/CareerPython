from typing import List, Optional

from core.database import DatabaseInterface
from src.candidate_bc.candidate.domain.entities import CandidateProject
from src.candidate_bc.candidate.domain.repositories.candidate_project_repository_interface import CandidateProjectRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from src.candidate_bc.candidate.infrastructure.models import CandidateProjectModel
from src.framework.infrastructure.repositories.base import BaseRepository


class SQLAlchemyCandidateProjectRepository(CandidateProjectRepositoryInterface):
    """Implementación de repositorio de proyectos de candidatos con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, CandidateProjectModel)

    def _to_domain(self, model: CandidateProjectModel) -> CandidateProject:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        from datetime import datetime
        return CandidateProject(
            id=CandidateProjectId.from_string(model.id),
            candidate_id=CandidateId.from_string(model.candidate_id),
            name=model.name,
            description=model.description,
            start_date=model.start_date,
            end_date=model.end_date,
            created_at=model.created_at or datetime.now(),
            updated_at=model.updated_at or datetime.now()
        )

    def _to_model(self, domain: CandidateProject) -> CandidateProjectModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        model = CandidateProjectModel()
        # Set all fields manually to avoid constructor issues
        model.id = domain.id.value
        model.candidate_id = domain.candidate_id.value
        model.name = domain.name
        model.description = domain.description
        model.start_date = domain.start_date
        model.end_date = domain.end_date
        model.created_at = domain.created_at
        model.updated_at = domain.updated_at
        return model

    def create(self, candidate_project: CandidateProject) -> CandidateProject:
        model = self._to_model(candidate_project)
        created_model = self.base_repo.create(model)
        return self._to_domain(created_model)

    def get_by_id(self, id: CandidateProjectId) -> Optional[CandidateProject]:
        model = self.base_repo.get_by_id(id)
        if model:
            return self._to_domain(model)
        return None

    def get_all(self, candidate_id: Optional[CandidateId] = None) -> List[CandidateProject]:
        with self.database.get_session() as session:
            query = session.query(CandidateProjectModel)
            if candidate_id:
                query = query.filter(CandidateProjectModel.candidate_id == candidate_id.value)
            models = query.all()
            return [self._to_domain(model) for model in models]

    def get_by_candidate_id(self, id: CandidateId) -> List[CandidateProject]:
        return self.get_all(candidate_id=id)

    def update(self, id: CandidateProjectId, candidate_project: CandidateProject) -> None:
        with self.database.get_session() as session:
            model = session.query(CandidateProjectModel).filter(
                CandidateProjectModel.id == id.value).first()
            if model:
                model.name = candidate_project.name
                model.description = candidate_project.description
                model.start_date = candidate_project.start_date
                model.end_date = candidate_project.end_date
                model.updated_at = candidate_project.updated_at
                session.commit()
                session.refresh(model)
            return None

    def delete(self, candidate_project_id: CandidateProjectId) -> bool:
        return self.base_repo.delete(candidate_project_id)
