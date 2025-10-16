from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.resume.domain.entities.resume import Resume
from src.resume.domain.enums.resume_type import ResumeType, ResumeStatus
from src.resume.domain.value_objects.resume_id import ResumeId


class ResumeRepositoryInterface(ABC):
    """Interface para el repositorio de Resume"""

    @abstractmethod
    def create(self, resume: Resume) -> Resume:
        """Crea un nuevo resume"""
        pass

    @abstractmethod
    def get_by_id(self, resume_id: ResumeId) -> Optional[Resume]:
        """Obtiene un resume por ID"""
        pass

    @abstractmethod
    def get_by_candidate_id(
            self,
            candidate_id: CandidateId,
            resume_type: Optional[ResumeType] = None,
            limit: Optional[int] = None
    ) -> List[Resume]:
        """Obtiene resumes por candidate ID"""
        pass

    @abstractmethod
    def update(self, resume: Resume) -> Resume:
        """Actualiza un resume"""
        pass

    @abstractmethod
    def delete(self, resume_id: ResumeId) -> bool:
        """Elimina un resume"""
        pass

    @abstractmethod
    def get_statistics_by_candidate(self, candidate_id: CandidateId) -> Dict[str, Any]:
        """Obtiene estadísticas de resumes por candidato"""
        pass

    @abstractmethod
    def get_all_by_status(self, status: ResumeStatus) -> List[Resume]:
        """Obtiene resumes por status"""
        pass

    @abstractmethod
    def bulk_delete(self, resume_ids: List[ResumeId]) -> int:
        """Elimina múltiples resumes y retorna el número eliminado"""
        pass
