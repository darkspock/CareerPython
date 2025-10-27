"""
List Public Job Positions Query
Phase 10: Public job board - returns only public positions
"""
from dataclasses import dataclass
from typing import Optional, List

from src.job_position.application.queries.job_position_dto import JobPositionDto
from src.job_position.domain.enums import JobPositionStatusEnum, WorkLocationTypeEnum, ContractTypeEnum
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.query_bus import Query
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListPublicJobPositionsQuery(Query):
    """
    Query to list public job positions (is_public=True, status=ACTIVE)
    No company_id filter - shows positions from all companies
    """
    job_category: Optional[JobCategoryEnum] = None
    work_location_type: Optional[WorkLocationTypeEnum] = None
    contract_type: Optional[ContractTypeEnum] = None
    location: Optional[str] = None
    search_term: Optional[str] = None
    limit: int = 50
    offset: int = 0


class ListPublicJobPositionsQueryHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: ListPublicJobPositionsQuery) -> List[JobPositionDto]:
        """
        Handle query for public job positions
        Only returns positions where is_public=True and status=ACTIVE
        """
        # Filter for public and active positions only
        job_positions = self.job_position_repository.find_by_filters(
            company_id=None,  # No company filter - show all companies
            status=JobPositionStatusEnum.ACTIVE,  # Only active positions
            job_category=query.job_category,
            work_location_type=query.work_location_type,
            contract_type=query.contract_type,
            location=query.location,
            search_term=query.search_term,
            limit=query.limit,
            offset=query.offset,
            is_public=True  # Only public positions
        )

        return [JobPositionDto.from_entity(jp) for jp in job_positions]
