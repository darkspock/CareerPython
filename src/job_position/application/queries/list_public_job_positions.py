"""
List Public Job Positions Query
Phase 10: Public job board - returns only public positions
"""
from dataclasses import dataclass
from typing import Optional, List

from src.job_position.application.queries.job_position_dto import JobPositionDto
from src.job_position.domain.enums import JobPositionVisibilityEnum
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListPublicJobPositionsQuery(Query):
    """
    Query to list public job positions (visibility=PUBLIC)
    No company_id filter - shows positions from all companies
    """
    job_category: Optional[JobCategoryEnum] = None
    search_term: Optional[str] = None
    limit: int = 50
    offset: int = 0


class ListPublicJobPositionsQueryHandler(QueryHandler[ListPublicJobPositionsQuery, List[JobPositionDto]]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: ListPublicJobPositionsQuery) -> List[JobPositionDto]:
        """
        Handle query for public job positions
        Only returns positions where visibility=PUBLIC
        """
        # Filter for public positions
        job_positions = self.job_position_repository.find_by_filters(
            company_id=None,  # No company filter - show all companies
            job_category=query.job_category,
            search_term=query.search_term,
            limit=query.limit,
            offset=query.offset,
            visibility=JobPositionVisibilityEnum.PUBLIC  # Only public positions
        )

        return [JobPositionDto.from_entity(jp) for jp in job_positions]
