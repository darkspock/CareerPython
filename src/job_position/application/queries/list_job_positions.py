from dataclasses import dataclass
from typing import Optional, List

from src.job_position.application.queries.job_position_dto import JobPositionDto
from src.job_position.domain.enums import JobPositionStatusEnum, WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.query_bus import Query
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListJobPositionsQuery(Query):
    company_id: Optional[str] = None
    status: Optional[JobPositionStatusEnum] = None
    job_category: Optional[JobCategoryEnum] = None
    work_location_type: Optional[WorkLocationTypeEnum] = None
    contract_type: Optional[ContractTypeEnum] = None
    location: Optional[str] = None
    search_term: Optional[str] = None
    limit: int = 50
    offset: int = 0


class ListJobPositionsQueryHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: ListJobPositionsQuery) -> List[JobPositionDto]:
        jobPositions = self.job_position_repository.find_by_filters(
            company_id=query.company_id,
            status=query.status,
            job_category=query.job_category,
            work_location_type=query.work_location_type,
            contract_type=query.contract_type,
            location=query.location,
            search_term=query.search_term,
            limit=query.limit,
            offset=query.offset
        )
        return [JobPositionDto.from_entity(jp) for jp in jobPositions]
