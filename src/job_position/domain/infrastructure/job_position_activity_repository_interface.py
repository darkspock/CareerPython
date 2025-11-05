"""Job Position Activity Repository Interface."""
from abc import ABC, abstractmethod
from typing import List

from src.job_position.domain.entities.job_position_activity import JobPositionActivity
from src.job_position.domain.value_objects import JobPositionActivityId, JobPositionId


class JobPositionActivityRepositoryInterface(ABC):
    """Job Position Activity repository interface"""

    @abstractmethod
    def save(self, activity: JobPositionActivity) -> None:
        """
        Save an activity
        
        Args:
            activity: JobPositionActivity entity to save
        """
        pass

    @abstractmethod
    def list_by_job_position(
        self,
        job_position_id: JobPositionId,
        limit: int = 50
    ) -> List[JobPositionActivity]:
        """
        List activities for a job position
        
        Args:
            job_position_id: ID of the job position
            limit: Maximum number of activities to return (default: 50)
            
        Returns:
            List[JobPositionActivity]: Activities ordered by created_at DESC
        """
        pass

