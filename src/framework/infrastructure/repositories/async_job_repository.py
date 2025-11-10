"""AsyncJob repository implementation."""

from datetime import datetime, timezone
from typing import List, Optional

from sqlalchemy import and_, func

from core.database import DatabaseInterface
from ..models.async_job_model import AsyncJobModel
from ...domain.entities.async_job import AsyncJob, AsyncJobId
from ...domain.enums.async_job import AsyncJobStatus, AsyncJobType
from ...domain.infrastructure.async_job_repository_interface import AsyncJobRepositoryInterface


class AsyncJobRepository(AsyncJobRepositoryInterface):
    """Implementation of AsyncJob repository."""

    def __init__(self, database: DatabaseInterface):
        self._database = database

    def save(self, async_job: AsyncJob) -> None:
        """Save an async job."""
        with self._database.get_session() as session:
            # Check if job already exists
            existing_job = session.query(AsyncJobModel).filter(
                AsyncJobModel.id == str(async_job.id)
            ).first()

            if existing_job:
                # Update existing job
                self._update_model_from_entity(existing_job, async_job)
            else:
                # Create new job
                job_model = self._entity_to_model(async_job)
                session.add(job_model)

            session.commit()

    def get_by_id(self, job_id: AsyncJobId) -> Optional[AsyncJob]:
        """Get async job by ID."""
        with self._database.get_session() as session:
            job_model = session.query(AsyncJobModel).filter(
                AsyncJobModel.id == str(job_id)
            ).first()

            if job_model:
                return self._model_to_entity(job_model)
            return None

    def get_by_entity(
            self,
            job_type: AsyncJobType,
            entity_type: str,
            entity_id: str
    ) -> Optional[AsyncJob]:
        """Get async job by entity information."""
        with self._database.get_session() as session:
            job_model = session.query(AsyncJobModel).filter(
                and_(
                    AsyncJobModel.job_type == job_type.value,
                    AsyncJobModel.entity_type == entity_type,
                    AsyncJobModel.entity_id == entity_id
                )
            ).order_by(AsyncJobModel.created_at.desc()).first()

            if job_model:
                return self._model_to_entity(job_model)
            return None

    def get_by_status(self, status: AsyncJobStatus) -> List[AsyncJob]:
        """Get async jobs by status."""
        with self._database.get_session() as session:
            job_models = session.query(AsyncJobModel).filter(
                AsyncJobModel.status == status.value
            ).all()

            return [self._model_to_entity(job_model) for job_model in job_models]

    def get_pending_jobs(self) -> List[AsyncJob]:
        """Get all pending jobs."""
        return self.get_by_status(AsyncJobStatus.PENDING)

    def get_processing_jobs(self) -> List[AsyncJob]:
        """Get all processing jobs."""
        return self.get_by_status(AsyncJobStatus.PROCESSING)

    def get_timed_out_jobs(self) -> List[AsyncJob]:
        """Get jobs that should be marked as timed out."""
        with self._database.get_session() as session:
            now = datetime.now(timezone.utc)

            # Get processing jobs that have exceeded their timeout
            job_models = session.query(AsyncJobModel).filter(
                and_(
                    AsyncJobModel.status == AsyncJobStatus.PROCESSING.value,
                    AsyncJobModel.started_at.isnot(None),
                    AsyncJobModel.started_at +
                    func.make_interval(seconds=AsyncJobModel.timeout_seconds) < now
                )
            ).all()

            return [self._model_to_entity(job_model) for job_model in job_models]

    def delete(self, job_id: AsyncJobId) -> None:
        """Delete an async job."""
        with self._database.get_session() as session:
            job_model = session.query(AsyncJobModel).filter(
                AsyncJobModel.id == str(job_id)
            ).first()

            if job_model:
                session.delete(job_model)
                session.commit()

    def _entity_to_model(self, async_job: AsyncJob) -> AsyncJobModel:
        """Convert entity to model."""
        return AsyncJobModel(
            id=str(async_job.id),
            job_type=async_job.job_type.value,
            entity_type=async_job.entity_type,
            entity_id=async_job.entity_id,
            status=async_job.status.value,
            progress=async_job.progress,
            message=async_job.message,
            started_at=async_job.started_at,
            completed_at=async_job.completed_at,
            results=async_job.results,
            error_message=async_job.error_message,
            job_metadata=async_job.metadata,
            timeout_seconds=async_job.timeout_seconds,
            created_at=async_job.created_at,
            updated_at=async_job.updated_at
        )

    def _model_to_entity(self, job_model: AsyncJobModel) -> AsyncJob:
        """Convert model to entity."""
        return AsyncJob(
            id=AsyncJobId(job_model.id),
            job_type=AsyncJobType(job_model.job_type),
            entity_type=job_model.entity_type,
            entity_id=job_model.entity_id,
            status=AsyncJobStatus(job_model.status),
            progress=job_model.progress,
            message=job_model.message,
            started_at=job_model.started_at,
            completed_at=job_model.completed_at,
            results=job_model.results,
            error_message=job_model.error_message,
            metadata=job_model.job_metadata,
            timeout_seconds=job_model.timeout_seconds,
            created_at=job_model.created_at,
            updated_at=job_model.updated_at
        )

    def _update_model_from_entity(self, job_model: AsyncJobModel, async_job: AsyncJob) -> None:
        """Update model from entity."""
        job_model.job_type = async_job.job_type.value
        job_model.entity_type = async_job.entity_type
        job_model.entity_id = async_job.entity_id
        job_model.status = async_job.status.value
        job_model.progress = async_job.progress
        job_model.message = async_job.message
        job_model.started_at = async_job.started_at
        job_model.completed_at = async_job.completed_at
        job_model.results = async_job.results
        job_model.error_message = async_job.error_message
        job_model.job_metadata = async_job.metadata
        job_model.timeout_seconds = async_job.timeout_seconds
        job_model.updated_at = async_job.updated_at
