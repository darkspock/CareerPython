from abc import ABC, abstractmethod
from typing import Optional, List, Any

from src.candidate_bc.candidate.domain.entities import Candidate
from src.candidate_bc.candidate.domain.enums import CandidateStatusEnum
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.auth_bc.user.domain.value_objects.UserId import UserId


class CandidateRepositoryInterface(ABC):
    """Interfaz para repositorio de candidatos"""

    @abstractmethod
    def create(self, candidate: Candidate) -> None:
        pass

    @abstractmethod
    def get_by_id(self, id: CandidateId) -> Optional[Candidate]:
        pass

    @abstractmethod
    def get_all(self, name: Optional[str] = None, phone: Optional[str] = None) -> List[Candidate]:
        pass

    @abstractmethod
    def update(self, candidate: Candidate) -> None:
        pass

    @abstractmethod
    def delete(self, candidate_id: CandidateId) -> bool:
        pass

    @abstractmethod
    def get_by_user_id(self, id: UserId) -> Optional[Candidate]:
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[Candidate]:
        pass

    @abstractmethod
    def admin_find_by_filters(self, name: Optional[str] = None,
                              email: Optional[str] = None,
                              phone: Optional[str] = None,
                              status: Optional[Any] = None,
                              job_category: Optional[Any] = None,
                              location: Optional[str] = None,
                              years_of_experience_min: Optional[int] = None,
                              years_of_experience_max: Optional[int] = None,
                              created_after: Optional[Any] = None,
                              created_before: Optional[Any] = None,
                              search_term: Optional[str] = None,
                              has_resume: Optional[bool] = None,
                              limit: int = 50, offset: int = 0) -> List[Candidate]:
        pass

    @abstractmethod
    def count_total(self) -> int:
        pass

    @abstractmethod
    def count_with_resume(self) -> int:
        pass

    @abstractmethod
    def count_recent(self, days: int) -> int:
        pass

    @abstractmethod
    def count_active(self) -> int:
        pass

    @abstractmethod
    def count_by_status(self, status: CandidateStatusEnum) -> int:
        pass
