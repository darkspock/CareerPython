"""CandidateStage repository interface"""
from abc import ABC, abstractmethod
from typing import List, Optional

from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_bc.candidate_application_stage.domain.entities.candidate_application_stage import \
    CandidateApplicationStage
from src.company_bc.candidate_application_stage.domain.value_objects.candidate_application_stage_id import \
    CandidateApplicationStageId
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


class CandidateStageRepositoryInterface(ABC):
    """Repository interface for CandidateStage aggregate"""

    @abstractmethod
    def save(self, candidate_stage: CandidateApplicationStage) -> None:
        """Save a candidate stage"""
        pass

    @abstractmethod
    def get_by_id(self, id: CandidateApplicationStageId) -> Optional[CandidateApplicationStage]:
        """Get candidate stage by ID"""
        pass

    @abstractmethod
    def list_by_candidate_application(
            self,
            candidate_application_id: CandidateApplicationId
    ) -> List[CandidateApplicationStage]:
        """Get all stages for a candidate application"""
        pass

    @abstractmethod
    def list_by_phase(self, phase_id: PhaseId) -> List[CandidateApplicationStage]:
        """Get all stages for a specific phase"""
        pass

    @abstractmethod
    def get_current_stage(
            self,
            candidate_application_id: CandidateApplicationId
    ) -> Optional[CandidateApplicationStage]:
        """Get the current (most recent uncompleted) stage for a candidate application"""
        pass

    @abstractmethod
    def delete(self, id: CandidateApplicationStageId) -> None:
        """Delete a candidate stage"""
        pass
