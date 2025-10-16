from abc import abstractmethod, ABC
from typing import Optional, List

from src.job_position.domain import JobPosition, JobPositionStatusEnum, WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.domain.value_objects import JobPositionId
from src.shared.domain.enums.job_category import JobCategoryEnum


class JobPositionRepositoryInterface(ABC):
    @abstractmethod
    def save(self, job_position: JobPosition) -> JobPosition:
        pass

    @abstractmethod
    def get_by_id(self, id: JobPositionId) -> Optional[JobPosition]:
        pass

    @abstractmethod
    def find_by_filters(self, company_id: Optional[str] = None,
                        status: Optional[JobPositionStatusEnum] = None,
                        job_category: Optional[JobCategoryEnum] = None,
                        work_location_type: Optional[WorkLocationTypeEnum] = None,
                        contract_type: Optional[ContractTypeEnum] = None,
                        location: Optional[str] = None,
                        search_term: Optional[str] = None,
                        limit: int = 50, offset: int = 0) -> List[JobPosition]:
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
