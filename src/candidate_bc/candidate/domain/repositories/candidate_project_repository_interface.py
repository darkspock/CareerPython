from abc import ABC, abstractmethod
from typing import List, Optional

from src.candidate_bc.candidate.domain.entities import CandidateProject
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.domain.value_objects.candidate_project_id import CandidateProjectId


class CandidateProjectRepositoryInterface(ABC):
    """Interfaz para repositorio de proyectos de candidatos"""

    @abstractmethod
    def create(self, candidate_project: CandidateProject) -> CandidateProject:
        pass

    @abstractmethod
    def get_by_id(self, id: CandidateProjectId) -> Optional[CandidateProject]:
        pass

    @abstractmethod
    def get_all(self, candidate_id: Optional[CandidateId] = None) -> List[CandidateProject]:
        pass

    @abstractmethod
    def update(self, id: CandidateProjectId, candidate_project: CandidateProject) -> None:
        pass

    @abstractmethod
    def delete(self, id: CandidateProjectId) -> bool:
        pass

    @abstractmethod
    def get_by_candidate_id(self, candidate_id: CandidateId) -> List[CandidateProject]:
        pass
