from abc import ABC, abstractmethod
from typing import Optional, List, TYPE_CHECKING

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId

if TYPE_CHECKING:
    from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId


class CandidateApplicationRepositoryInterface(ABC):
    """Interface para el repositorio de aplicaciones de candidatos"""

    @abstractmethod
    def save(self, candidate_application: CandidateApplication) -> None:
        """Guardar una aplicación"""
        pass

    @abstractmethod
    def get_by_id(self, application_id: CandidateApplicationId) -> Optional[CandidateApplication]:
        """Obtener aplicación por ID"""
        pass

    @abstractmethod
    def get_by_candidate_and_position(
            self,
            candidate_id: CandidateId,
            job_position_id: JobPositionId
    ) -> Optional[CandidateApplication]:
        """Obtener aplicación por candidato y posición"""
        pass

    @abstractmethod
    def get_applications_by_candidate(self, candidate_id: CandidateId) -> List[CandidateApplication]:
        """Obtener todas las aplicaciones de un candidato"""
        pass

    @abstractmethod
    def get_by_candidate_id(
            self,
            candidate_id: CandidateId,
            status_filter: Optional['ApplicationStatusEnum'] = None,
            limit: Optional[int] = None
    ) -> List[CandidateApplication]:
        """Obtener aplicaciones de un candidato con filtros"""
        pass

    @abstractmethod
    def get_applications_by_position(self, job_position_id: JobPositionId) -> List[CandidateApplication]:
        """Obtener todas las aplicaciones para una posición"""
        pass

    @abstractmethod
    def delete(self, application_id: CandidateApplicationId) -> None:
        """Eliminar aplicación"""
        pass
