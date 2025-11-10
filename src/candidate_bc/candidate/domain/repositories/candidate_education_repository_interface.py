from abc import abstractmethod, ABC
from typing import Optional, List

from src.candidate_bc.candidate.domain.entities import CandidateEducation
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


class CandidateEducationRepositoryInterface(ABC):
    """Interfaz para repositorio de educación de candidatos"""

    @abstractmethod
    def create(self, candidate_education: CandidateEducation) -> CandidateEducation:
        pass

    @abstractmethod
    def get_by_id(self, candidate_education_id: CandidateEducationId) -> Optional[CandidateEducation]:
        pass

    @abstractmethod
    def get_all(self, candidate_id: Optional[CandidateId] = None) -> List[CandidateEducation]:
        pass

    @abstractmethod
    def update(self, id: CandidateEducationId, candidate_education: CandidateEducation) -> Optional[CandidateEducation]:
        pass

    @abstractmethod
    def delete(self, id: CandidateEducationId) -> bool:
        pass

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: CandidateId) -> List[CandidateEducation]:
        pass
