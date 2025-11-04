from dataclasses import dataclass
from typing import Optional, List

from src.job_position.application.queries.job_position_dto import JobPositionDto
from src.job_position.domain.enums import JobPositionStatusEnum, JobPositionVisibilityEnum
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.query_bus import Query
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListJobPositionsQuery(Query):
    """Query to list job positions - simplified (removed fields are in custom_fields_values)"""
    company_id: Optional[str] = None
    status: Optional[JobPositionStatusEnum] = None  # TODO: Filtering by status now requires workflow repository
    job_category: Optional[JobCategoryEnum] = None
    search_term: Optional[str] = None
    visibility: Optional[JobPositionVisibilityEnum] = None  # New filter for visibility
    limit: int = 50
    offset: int = 0


class ListJobPositionsQueryHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: ListJobPositionsQuery) -> List[JobPositionDto]:
        """Handle query - simplified filters"""
        jobPositions = self.job_position_repository.find_by_filters(
            company_id=query.company_id,
            status=query.status,  # TODO: This will require workflow repository to map stage to status
            job_category=query.job_category,
            search_term=query.search_term,
            visibility=query.visibility,
            limit=query.limit,
            offset=query.offset
        )
        return [JobPositionDto.from_entity(jp) for jp in jobPositions]
