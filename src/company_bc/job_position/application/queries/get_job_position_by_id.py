from dataclasses import dataclass
from typing import Optional

from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetJobPositionByIdQuery(Query):
    id: JobPositionId


class GetJobPositionByIdQueryHandler(QueryHandler[GetJobPositionByIdQuery, Optional[JobPositionDto]]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: GetJobPositionByIdQuery) -> Optional[JobPositionDto]:
        job_position = self.job_position_repository.get_by_id(query.id)
        if not job_position:
            return None

        return JobPositionDto.from_entity(job_position)
