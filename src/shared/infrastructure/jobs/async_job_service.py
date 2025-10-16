"""AsyncJobService for managing asynchronous jobs."""

from typing import Any, Dict, List, Optional

from ...domain.entities.async_job import AsyncJob, AsyncJobId
from ...domain.enums.async_job import AsyncJobStatus, AsyncJobType
from ...domain.infrastructure.async_job_repository_interface import AsyncJobRepositoryInterface


class AsyncJobService:
    """Service for managing async jobs."""

    def __init__(self, repository: AsyncJobRepositoryInterface):
        self._repository = repository

    def create_job(
            self,
            id: AsyncJobId,
            job_type: AsyncJobType,
            entity_type: Optional[str] = None,
            entity_id: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None,
            timeout_seconds: int = 30
    ) -> None:
        """Create a new async job and return its ID."""
        job = AsyncJob.create(
            id=id,
            job_type=job_type,
            entity_type=entity_type,
            entity_id=entity_id,
            metadata=metadata,
            timeout_seconds=timeout_seconds
        )

        self._repository.save(job)

    def update_job_status(
            self,
            job_id: str,
            status: AsyncJobStatus,
            progress: int = 0,
            message: Optional[str] = None
    ) -> None:
        """Update job status and progress."""
        job = self._repository.get_by_id(AsyncJobId(job_id))
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")

        if status == AsyncJobStatus.PROCESSING:
            if job.status == AsyncJobStatus.PENDING:
                job.start_processing(message)
            else:
                job.update_progress(progress, message)
        elif status == AsyncJobStatus.COMPLETED:
            job.update_progress(progress, message)
        elif status == AsyncJobStatus.FAILED:
            if message:
                job.fail(message)
        elif status == AsyncJobStatus.TIMEOUT:
            job.timeout()

        self._repository.save(job)

    def complete_job(
            self,
            job_id: str,
            results: Optional[Dict[str, Any]] = None
    ) -> None:
        """Mark job as completed with results."""
        job = self._repository.get_by_id(AsyncJobId(job_id))
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")

        job.complete(results)
        self._repository.save(job)

    def fail_job(self, job_id: str, error_message: str) -> None:
        """Mark job as failed with error message."""
        job = self._repository.get_by_id(AsyncJobId(job_id))
        if not job:
            raise ValueError(f"Job with ID {job_id} not found")

        job.fail(error_message)
        self._repository.save(job)

    def get_job_status(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job status information."""
        job = self._repository.get_by_id(AsyncJobId(job_id))
        if not job:
            return None

        return {
            "job_id": str(job.id),
            "job_type": job.job_type.value,
            "entity_type": job.entity_type,
            "entity_id": job.entity_id,
            "status": job.status.value,
            "progress": job.progress,
            "message": job.message,
            "started_at": job.started_at.isoformat() if job.started_at else None,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None,
            "results": job.results,
            "error_message": job.error_message,
            "timeout_seconds": job.timeout_seconds,
            "estimated_time_remaining": job.get_estimated_time_remaining(),
            "created_at": job.created_at.isoformat(),
            "updated_at": job.updated_at.isoformat()
        }

    def get_job_by_entity(
            self,
            job_type: AsyncJobType,
            entity_type: str,
            entity_id: str
    ) -> Optional[Dict[str, Any]]:
        """Get job by entity information."""
        job = self._repository.get_by_entity(job_type, entity_type, entity_id)
        if not job:
            return None

        return self.get_job_status(str(job.id))

    def get_job_results(self, job_id: str) -> Optional[Dict[str, Any]]:
        """Get job results if completed."""
        job = self._repository.get_by_id(AsyncJobId(job_id))
        if not job or not job.is_finished():
            return None

        return {
            "job_id": str(job.id),
            "job_type": job.job_type.value,
            "status": job.status.value,
            "success": job.status == AsyncJobStatus.COMPLETED,
            "results": job.results,
            "error_message": job.error_message,
            "completed_at": job.completed_at.isoformat() if job.completed_at else None
        }

    def cleanup_old_jobs(self, older_than_hours: int = 24) -> int:
        """Clean up old completed/failed jobs."""
        # This would need to be implemented in the repository
        # For now, just return 0
        return 0

    def get_pending_jobs(self) -> List[Dict[str, Any]]:
        """Get all pending jobs."""
        jobs = self._repository.get_pending_jobs()
        statuses = [self.get_job_status(str(job.id)) for job in jobs]
        return [status for status in statuses if status is not None]

    def get_processing_jobs(self) -> List[Dict[str, Any]]:
        """Get all processing jobs."""
        jobs = self._repository.get_processing_jobs()
        statuses = [self.get_job_status(str(job.id)) for job in jobs]
        return [status for status in statuses if status is not None]

    def mark_timed_out_jobs(self) -> int:
        """Mark jobs that have exceeded their timeout as timed out."""
        timed_out_jobs = self._repository.get_timed_out_jobs()
        count = 0

        for job in timed_out_jobs:
            job.timeout()
            self._repository.save(job)
            count += 1

        return count
