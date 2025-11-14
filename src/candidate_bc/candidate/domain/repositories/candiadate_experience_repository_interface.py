from abc import ABC, abstractmethod
from typing import Optional, List, Dict, Any

from src.candidate_bc.candidate.domain.entities import CandidateExperience
from src.candidate_bc.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


class CandidateExperienceRepositoryInterface(ABC):
    """Interfaz para repositorio de experiencia laboral de candidatos"""

    @abstractmethod
    def create(self, candidate_experience: CandidateExperience) -> CandidateExperience:
        pass

    @abstractmethod
    def get_by_id(self, id: CandidateExperienceId) -> Optional[CandidateExperience]:
        pass

    @abstractmethod
    def get_all(self, candidate_id: Optional[CandidateId] = None) -> List[CandidateExperience]:
        pass

    @abstractmethod
    def update(self, id: CandidateExperienceId, candidate_experience_data: Dict[str, Any]) -> Optional[
        CandidateExperience]:
        pass

    @abstractmethod
    def delete(self, id: CandidateExperienceId) -> bool:
        pass

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: CandidateId) -> List[CandidateExperience]:
        pass
