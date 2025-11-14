"""AsyncJob domain entity."""

from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Any, Dict, Optional

from ..enums.async_job import AsyncJobStatus, AsyncJobType
from ..value_objects.base_id import BaseId


class AsyncJobId(BaseId):
    """Value object for AsyncJob ID."""
    pass


@dataclass
class AsyncJob:
    """AsyncJob domain entity for managing asynchronous job processing."""

    id: AsyncJobId
    job_type: AsyncJobType
    entity_type: Optional[str]
    entity_id: Optional[str]
    status: AsyncJobStatus
    progress: int
    message: Optional[str]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    results: Optional[Dict[str, Any]]
    error_message: Optional[str]
    metadata: Optional[Dict[str, Any]]
    timeout_seconds: int
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
            id: AsyncJobId,
            job_type: AsyncJobType,
            entity_type: Optional[str] = None,
            entity_id: Optional[str] = None,
            metadata: Optional[Dict[str, Any]] = None,
            timeout_seconds: int = 30
    ) -> "AsyncJob":
        """Create a new AsyncJob."""
        now = datetime.now(timezone.utc)

        return AsyncJob(
            id=id,
            job_type=job_type,
            entity_type=entity_type,
            entity_id=entity_id,
            status=AsyncJobStatus.PENDING,
            progress=0,
            message=None,
            started_at=None,
            completed_at=None,
            results=None,
            error_message=None,
            metadata=metadata or {},
            timeout_seconds=timeout_seconds,
            created_at=now,
            updated_at=now
        )

    def start_processing(self, message: Optional[str] = None) -> None:
        """Mark job as processing."""
        now = datetime.now(timezone.utc)
        self.status = AsyncJobStatus.PROCESSING
        self.started_at = now
        self.updated_at = now
        if message:
            self.message = message

    def update_progress(self, progress: int, message: Optional[str] = None) -> None:
        """Update job progress."""
        if not 0 <= progress <= 100:
            raise ValueError("Progress must be between 0 and 100")

        self.progress = progress
        self.updated_at = datetime.now(timezone.utc)
        if message:
            self.message = message

    def complete(self, results: Optional[Dict[str, Any]] = None) -> None:
        """Mark job as completed."""
        now = datetime.now(timezone.utc)
        self.status = AsyncJobStatus.COMPLETED
        self.progress = 100
        self.completed_at = now
        self.updated_at = now
        if results:
            self.results = results

    def fail(self, error_message: str) -> None:
        """Mark job as failed."""
        now = datetime.now(timezone.utc)
        self.status = AsyncJobStatus.FAILED
        self.completed_at = now
        self.updated_at = now
        self.error_message = error_message

    def timeout(self) -> None:
        """Mark job as timed out."""
        now = datetime.now(timezone.utc)
        self.status = AsyncJobStatus.TIMEOUT
        self.completed_at = now
        self.updated_at = now
        self.error_message = f"Job timed out after {self.timeout_seconds} seconds"

    def is_finished(self) -> bool:
        """Check if job is in a finished state."""
        return self.status in [
            AsyncJobStatus.COMPLETED,
            AsyncJobStatus.FAILED,
            AsyncJobStatus.TIMEOUT
        ]

    def is_processing(self) -> bool:
        """Check if job is currently processing."""
        return self.status == AsyncJobStatus.PROCESSING

    def get_estimated_time_remaining(self) -> Optional[int]:
        """Calculate estimated time remaining in seconds."""
        if not self.is_processing() or not self.started_at or self.progress == 0:
            return None

        now = datetime.now(timezone.utc)
        elapsed_seconds = (now - self.started_at).total_seconds()

        if self.progress >= 100:
            return 0

        # Estimate based on current progress
        estimated_total_time = elapsed_seconds * (100 / self.progress)
        estimated_remaining = estimated_total_time - elapsed_seconds

        # Don't exceed the timeout
        max_remaining = self.timeout_seconds - elapsed_seconds
        return min(int(estimated_remaining), int(max_remaining))
