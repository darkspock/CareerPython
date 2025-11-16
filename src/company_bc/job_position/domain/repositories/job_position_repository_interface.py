from abc import abstractmethod, ABC
from typing import Optional, List, Union

from src.company_bc.company.domain import CompanyId
from src.company_bc.job_position.domain import JobPosition, JobPositionStatusEnum
from src.company_bc.job_position.domain.enums.job_position_visibility import JobPositionVisibilityEnum
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.framework.domain.enums.job_category import JobCategoryEnum


class JobPositionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, job_position: JobPosition) -> JobPosition:
        pass

    @abstractmethod
    def get_by_id(self, id: JobPositionId) -> Optional[JobPosition]:
        pass

    def find_published(self, company_id: CompanyId) -> List[JobPosition]:
        pass

    @abstractmethod
    def find_by_filters(self, company_id: Optional[str] = None,
                        status: Optional[Union[JobPositionStatusEnum, List[JobPositionStatusEnum]]] = None,
                        job_category: Optional[JobCategoryEnum] = None,
                        search_term: Optional[str] = None,
                        limit: int = 50, offset: int = 0,
                        visibility: Optional[JobPositionVisibilityEnum] = None) -> List[JobPosition]:
        """Find job positions by filters

        Args:
            status: Single status or list of statuses to filter by (deprecated, use stage filtering)
            visibility: Visibility filter (hidden, internal, public)
        """
        pass

    @abstractmethod
    def count_by_filters(self, company_id: Optional[str] = None,
                         status: Optional[Union[JobPositionStatusEnum, List[JobPositionStatusEnum]]] = None,
                         job_category: Optional[JobCategoryEnum] = None,
                         search_term: Optional[str] = None,
                         visibility: Optional[JobPositionVisibilityEnum] = None) -> int:
        """Count job positions matching the filters
        
        Args:
            status: Single status or list of statuses to filter by (deprecated, use stage filtering)
            visibility: Visibility filter (hidden, internal, public)
        """
        pass

    @abstractmethod
    def find_by_public_slug(self, public_slug: str) -> Optional[JobPosition]:
        """Phase 10: Find job position by public slug"""
        pass

    @abstractmethod
    def count_by_status(self, status: JobPositionStatusEnum) -> int:
        pass

    @abstractmethod
    def count_total(self) -> int:
        pass

    @abstractmethod
    def count_recent(self, days: int = 30) -> int:
        pass

    @abstractmethod
    def count_active_by_company_id(self, company_id: str) -> int:
        pass

    @abstractmethod
    def delete(self, id: JobPositionId) -> bool:
        pass
