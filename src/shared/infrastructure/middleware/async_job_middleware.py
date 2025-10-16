"""Dramatiq middleware for AsyncJob integration."""

from typing import Any, Optional

import dramatiq
from dramatiq import Middleware, Message
from dramatiq.logging import get_logger

from core.database import database
from ..jobs.async_job_service import AsyncJobService
from ..repositories.async_job_repository import AsyncJobRepository
from ...domain.enums.async_job import AsyncJobStatus

logger = get_logger(__name__)


class AsyncJobMiddleware(Middleware):
    """Middleware to integrate Dramatiq with AsyncJobService."""

    def __init__(self) -> None:
        self.async_job_service: Optional[AsyncJobService] = None

    def _get_async_job_service(self) -> AsyncJobService:
        """Get or create AsyncJobService instance."""
        if self.async_job_service is None:
            repository = AsyncJobRepository(database)
            self.async_job_service = AsyncJobService(repository)
        return self.async_job_service

    def before_process_message(self, broker: dramatiq.Broker, message: Message) -> None:
        """Called before processing a message."""
        job_id = message.kwargs.get('job_id')
        if not job_id:
            return

        try:
            async_job_service = self._get_async_job_service()
            async_job_service.update_job_status(
                job_id=job_id,
                status=AsyncJobStatus.PROCESSING,
                progress=0,
                message="Starting job execution..."
            )
            logger.info(f"Job {job_id} marked as processing")
        except Exception as e:
            logger.error(f"Failed to update job status to processing for {job_id}: {e}")

    def after_process_message(
            self,
            broker: dramatiq.Broker,
            message: Message,
            *,
            result: Any = None,
            exception: Optional[Exception] = None
    ) -> None:
        """Called after processing a message."""
        job_id = message.kwargs.get('job_id')
        if not job_id:
            return

        try:
            async_job_service = self._get_async_job_service()

            if exception:
                # Job failed
                error_message = f"Job failed with exception: {str(exception)}"
                async_job_service.fail_job(job_id, error_message)
                logger.error(f"Job {job_id} failed: {error_message}")
            else:
                # Job succeeded - the actual completion should be handled by the actor itself
                # This is just a safety net in case the actor doesn't complete the job
                job_status = async_job_service.get_job_status(job_id)
                if job_status and job_status['status'] == AsyncJobStatus.PROCESSING.value:
                    async_job_service.complete_job(job_id, {"completed_by": "middleware_fallback"})
                    logger.info(f"Job {job_id} completed by middleware fallback")

        except Exception as e:
            logger.error(f"Failed to update job status after processing for {job_id}: {e}")

    def after_message_failure(
            self,
            broker: dramatiq.Broker,
            message: Message,
            exception: Exception
    ) -> None:
        """Called after a message fails permanently."""
        job_id = message.kwargs.get('job_id')
        if not job_id:
            return

        try:
            async_job_service = self._get_async_job_service()
            error_message = f"Job permanently failed after retries: {str(exception)}"
            async_job_service.fail_job(job_id, error_message)
            logger.error(f"Job {job_id} permanently failed: {error_message}")
        except Exception as e:
            logger.error(f"Failed to mark job as permanently failed for {job_id}: {e}")

    def after_skip_message(
            self,
            broker: dramatiq.Broker,
            message: Message
    ) -> None:
        """Called after skipping a message."""
        job_id = message.kwargs.get('job_id')
        if job_id:
            logger.warning(f"Job {job_id} was skipped")
