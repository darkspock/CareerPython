from dataclasses import dataclass
from typing import Optional, List

from src.company_bc.company.domain import CompanyId
from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.company_bc.job_position.domain.enums import JobPositionVisibilityEnum
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class ListPublishedJobPositionsQuery(Query):
    """
    Query to list published job positions
    """
    company_id: CompanyId


class ListPublishedJobPositionsQueryHandler(QueryHandler[ListPublishedJobPositionsQuery, List[JobPositionDto]]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: ListPublishedJobPositionsQuery) -> List[JobPositionDto]:
        # Filter for public positions
        job_positions = self.job_position_repository.find_published(
            company_id=query.company_id,  # No company filter - show all companies
        )

        return [JobPositionDto.from_entity(jp) for jp in job_positions]
