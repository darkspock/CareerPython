"""Job Position Activity Repository Implementation."""
from typing import List

from sqlalchemy.orm import Session

from src.job_position.domain.entities.job_position_activity import JobPositionActivity
from src.job_position.domain.enums.activity_type_enum import ActivityTypeEnum
from src.job_position.domain.value_objects import (
    JobPositionActivityId,
    JobPositionId,
)
from src.job_position.domain.infrastructure.job_position_activity_repository_interface import (
    JobPositionActivityRepositoryInterface
)
from src.job_position.infrastructure.models.job_position_activity_model import JobPositionActivityModel
from src.company.domain.value_objects.company_user_id import CompanyUserId
from core.database import SQLAlchemyDatabase


class JobPositionActivityRepository(JobPositionActivityRepositoryInterface):
    """SQLAlchemy implementation of JobPositionActivityRepositoryInterface"""

    def __init__(self, database: SQLAlchemyDatabase):
        self.database = database

    def _get_session(self) -> Session:
        """Get database session"""
        return self.database.get_session()

    def _to_domain(self, model: JobPositionActivityModel) -> JobPositionActivity:
        """Convert model to domain entity"""
        return JobPositionActivity(
            id=JobPositionActivityId.from_string(model.id),
            job_position_id=JobPositionId.from_string(model.job_position_id),
            activity_type=ActivityTypeEnum(model.activity_type),
            description=model.description,
            performed_by_user_id=CompanyUserId.from_string(model.performed_by_user_id),
            metadata=model.activity_metadata,
            created_at=model.created_at,
        )

    def _to_model(self, entity: JobPositionActivity) -> JobPositionActivityModel:
        """Convert domain entity to model"""
        return JobPositionActivityModel(
            id=str(entity.id),
            job_position_id=str(entity.job_position_id),
            activity_type=entity.activity_type.value,
            description=entity.description,
            performed_by_user_id=str(entity.performed_by_user_id),
            activity_metadata=entity.metadata,
            created_at=entity.created_at,
        )

    def save(self, activity: JobPositionActivity) -> None:
        """Save an activity"""
        session = self._get_session()
        model = self._to_model(activity)
        session.add(model)
        session.commit()

    def list_by_job_position(
        self,
        job_position_id: JobPositionId,
        limit: int = 50
    ) -> List[JobPositionActivity]:
        """List activities for a job position"""
        session = self._get_session()
        models = session.query(JobPositionActivityModel).filter(
            JobPositionActivityModel.job_position_id == str(job_position_id)
        ).order_by(JobPositionActivityModel.created_at.desc()).limit(limit).all()

        return [self._to_domain(model) for model in models]

