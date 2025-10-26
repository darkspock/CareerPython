from typing import Optional, List

from sqlalchemy.orm import Session

from core.database import DatabaseInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.candidate_application.domain.enums.task_status import TaskStatus
from src.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared.infrastructure.repositories.base import BaseRepository


class SQLAlchemyCandidateApplicationRepository(CandidateApplicationRepositoryInterface):
    """Implementación de repositorio de aplicaciones de candidatos con SQLAlchemy"""

    def __init__(self, database: DatabaseInterface):
        self.database = database
        self.base_repo = BaseRepository(database, CandidateApplicationModel)

    def _to_domain(self, model: CandidateApplicationModel) -> CandidateApplication:
        """Convierte modelo de SQLAlchemy a entidad de dominio"""
        return CandidateApplication(
            id=CandidateApplicationId(model.id),
            candidate_id=CandidateId(model.candidate_id),
            job_position_id=JobPositionId(model.job_position_id),
            application_status=ApplicationStatusEnum(model.application_status),
            applied_at=model.applied_at,
            updated_at=model.updated_at,
            notes=model.notes,
            # Phase 5: Workflow stage tracking fields
            current_stage_id=model.current_stage_id,
            stage_entered_at=model.stage_entered_at,
            stage_deadline=model.stage_deadline,
            task_status=TaskStatus(model.task_status) if model.task_status else TaskStatus.PENDING
        )

    def _to_model(self, entity: CandidateApplication) -> CandidateApplicationModel:
        """Convierte entidad de dominio a modelo de SQLAlchemy"""
        from datetime import datetime
        return CandidateApplicationModel(
            id=entity.id.value,
            candidate_id=entity.candidate_id.value,
            job_position_id=entity.job_position_id.value,
            application_status=entity.application_status,  # SQLAlchemy will handle enum conversion
            applied_at=entity.applied_at,
            updated_at=datetime.utcnow(),  # Always set to current time when saving
            notes=entity.notes,
            # Phase 5: Workflow stage tracking fields
            current_stage_id=entity.current_stage_id,
            stage_entered_at=entity.stage_entered_at,
            stage_deadline=entity.stage_deadline,
            task_status=entity.task_status  # SQLAlchemy will handle enum conversion
        )

    def save(self, candidate_application: CandidateApplication) -> None:
        """Guardar una aplicación"""
        from datetime import datetime
        session: Session = self.database.get_session()
        try:
            existing_model = session.query(CandidateApplicationModel).filter_by(
                id=candidate_application.id.value
            ).first()

            if existing_model:
                # Update existing
                existing_model.candidate_id = candidate_application.candidate_id.value
                existing_model.job_position_id = candidate_application.job_position_id.value
                existing_model.application_status = candidate_application.application_status  # SQLAlchemy handles enum
                existing_model.applied_at = candidate_application.applied_at
                existing_model.updated_at = datetime.utcnow()  # Always set to current time
                existing_model.notes = candidate_application.notes
                # Phase 5: Update workflow stage tracking fields
                existing_model.current_stage_id = candidate_application.current_stage_id
                existing_model.stage_entered_at = candidate_application.stage_entered_at
                existing_model.stage_deadline = candidate_application.stage_deadline
                existing_model.task_status = candidate_application.task_status  # SQLAlchemy handles enum
            else:
                # Create new
                model = self._to_model(candidate_application)
                session.add(model)

            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, application_id: CandidateApplicationId) -> Optional[CandidateApplication]:
        """Obtener aplicación por ID"""
        model = self.base_repo.get_by_id(application_id)
        return self._to_domain(model) if model else None

    def get_by_candidate_and_position(
            self,
            candidate_id: CandidateId,
            job_position_id: JobPositionId
    ) -> Optional[CandidateApplication]:
        """Obtener aplicación por candidato y posición"""
        session: Session = self.database.get_session()
        try:
            model = session.query(CandidateApplicationModel).filter_by(
                candidate_id=candidate_id.value,
                job_position_id=job_position_id.value
            ).first()
            return self._to_domain(model) if model else None
        finally:
            session.close()

    def get_applications_by_candidate(self, candidate_id: CandidateId) -> List[CandidateApplication]:
        """Obtener todas las aplicaciones de un candidato"""
        session: Session = self.database.get_session()
        try:
            models = session.query(CandidateApplicationModel).filter_by(
                candidate_id=candidate_id.value
            ).all()
            return [self._to_domain(model) for model in models]
        finally:
            session.close()

    def get_by_candidate_id(
            self,
            candidate_id: CandidateId,
            status_filter: Optional[ApplicationStatusEnum] = None,
            limit: Optional[int] = None
    ) -> List[CandidateApplication]:
        """Obtener aplicaciones de un candidato con filtros"""
        session: Session = self.database.get_session()
        try:
            query = session.query(CandidateApplicationModel).filter_by(
                candidate_id=candidate_id.value
            )

            if status_filter:
                query = query.filter(CandidateApplicationModel.application_status == status_filter)

            if limit:
                query = query.limit(limit)

            models = query.all()
            return [self._to_domain(model) for model in models]
        finally:
            session.close()

    def get_applications_by_position(self, job_position_id: JobPositionId) -> List[CandidateApplication]:
        """Obtener todas las aplicaciones para una posición"""
        session: Session = self.database.get_session()
        try:
            models = session.query(CandidateApplicationModel).filter_by(
                job_position_id=job_position_id.value
            ).all()
            return [self._to_domain(model) for model in models]
        finally:
            session.close()

    def delete(self, application_id: CandidateApplicationId) -> None:
        """Eliminar aplicación"""
        session: Session = self.database.get_session()
        try:
            model = session.query(CandidateApplicationModel).filter_by(
                id=application_id.value
            ).first()
            if model:
                session.delete(model)
                session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()
