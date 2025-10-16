"""AsyncJob repository interface."""

from abc import ABC, abstractmethod
from typing import List, Optional

from ..entities.async_job import AsyncJob, AsyncJobId
from ..enums.async_job import AsyncJobStatus, AsyncJobType


class AsyncJobRepositoryInterface(ABC):
    """Interface for AsyncJob repository."""

    @abstractmethod
    def save(self, async_job: AsyncJob) -> None:
        """Save an async job."""
        pass

    @abstractmethod
    def get_by_id(self, job_id: AsyncJobId) -> Optional[AsyncJob]:
        """Get async job by ID."""
        pass

    @abstractmethod
    def get_by_entity(
            self,
            job_type: AsyncJobType,
            entity_type: str,
            entity_id: str
    ) -> Optional[AsyncJob]:
        """Get async job by entity information."""
        pass

    @abstractmethod
    def get_by_status(self, status: AsyncJobStatus) -> List[AsyncJob]:
        """Get async jobs by status."""
        pass

    @abstractmethod
    def get_pending_jobs(self) -> List[AsyncJob]:
        """Get all pending jobs."""
        pass

    @abstractmethod
    def get_processing_jobs(self) -> List[AsyncJob]:
        """Get all processing jobs."""
        pass

    @abstractmethod
    def get_timed_out_jobs(self) -> List[AsyncJob]:
        """Get jobs that should be marked as timed out."""
        pass

    @abstractmethod
    def delete(self, job_id: AsyncJobId) -> None:
        """Delete an async job."""
        pass
