"""JobPositionStage repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.company_bc.job_position.domain.entities.job_position_stage import JobPositionStage
from src.company_bc.job_position.domain.value_objects.job_position_stage_id import JobPositionStageId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


class JobPositionStageRepositoryInterface(ABC):
    """Repository interface for JobPositionStage aggregate"""

    @abstractmethod
    def save(self, job_position_stage: JobPositionStage) -> None:
        """Save a job position stage"""
        pass

    @abstractmethod
    def get_by_id(self, id: JobPositionStageId) -> Optional[JobPositionStage]:
        """Get job position stage by ID"""
        pass

    @abstractmethod
    def list_by_job_position(
        self,
        job_position_id: JobPositionId
    ) -> List[JobPositionStage]:
        """Get all stages for a job position"""
        pass

    @abstractmethod
    def list_by_phase(self, phase_id: PhaseId) -> List[JobPositionStage]:
        """Get all stages for a specific phase"""
        pass

    @abstractmethod
    def get_current_by_job_position(
        self,
        job_position_id: JobPositionId
    ) -> Optional[JobPositionStage]:
        """Get the current (most recent uncompleted) stage for a job position"""
        pass

    @abstractmethod
    def delete(self, id: JobPositionStageId) -> None:
        """Delete a job position stage"""
        pass

