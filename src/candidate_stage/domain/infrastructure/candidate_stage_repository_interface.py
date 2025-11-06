"""CandidateStage repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.candidate_stage.domain.entities.candidate_stage import CandidateStage
from src.candidate_stage.domain.value_objects.candidate_stage_id import CandidateStageId
from src.phase.domain.value_objects.phase_id import PhaseId


class CandidateStageRepositoryInterface(ABC):
    """Repository interface for CandidateStage aggregate"""

    @abstractmethod
    def save(self, candidate_stage: CandidateStage) -> None:
        """Save a candidate stage"""
        pass

    @abstractmethod
    def get_by_id(self, id: CandidateStageId) -> Optional[CandidateStage]:
        """Get candidate stage by ID"""
        pass

    @abstractmethod
    def list_by_candidate_application(
            self,
            candidate_application_id: CandidateApplicationId
    ) -> List[CandidateStage]:
        """Get all stages for a candidate application"""
        pass

    @abstractmethod
    def list_by_phase(self, phase_id: PhaseId) -> List[CandidateStage]:
        """Get all stages for a specific phase"""
        pass

    @abstractmethod
    def get_current_stage(
            self,
            candidate_application_id: CandidateApplicationId
    ) -> Optional[CandidateStage]:
        """Get the current (most recent uncompleted) stage for a candidate application"""
        pass

    @abstractmethod
    def delete(self, id: CandidateStageId) -> None:
        """Delete a candidate stage"""
        pass
