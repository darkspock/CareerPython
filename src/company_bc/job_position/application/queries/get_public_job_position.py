"""
Get Public Job Position Query
Phase 10: Get a single public position by slug or ID
"""
from dataclasses import dataclass

from src.company_bc.job_position.application.queries.job_position_dto import JobPositionDto
from src.company_bc.job_position.domain.enums import JobPositionVisibilityEnum
from src.company_bc.job_position.domain.exceptions import JobPositionNotFoundError
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetPublicJobPositionQuery(Query):
    """
    Query to get a single public job position by slug or ID
    """
    slug_or_id: str


class GetPublicJobPositionQueryHandler(QueryHandler[GetPublicJobPositionQuery, JobPositionDto]):
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def handle(self, query: GetPublicJobPositionQuery) -> JobPositionDto:
        """
        Handle query for a single public job position
        First tries to find by public_slug, then by ID
        Only returns positions where visibility=PUBLIC
        """
        job_position = None

        # Try to find by public_slug first
        try:
            job_position = self.job_position_repository.find_by_public_slug(query.slug_or_id)
        except (JobPositionNotFoundError, AttributeError):
            # Not found by slug or method doesn't exist, will try by ID below
            pass

        # If not found by slug (either None or exception), try by ID
        if not job_position:
            from src.company_bc.job_position.domain.value_objects import JobPositionId
            try:
                position_id = JobPositionId.from_string(query.slug_or_id)
                job_position = self.job_position_repository.get_by_id(position_id)
            except (JobPositionNotFoundError, ValueError):
                raise JobPositionNotFoundError(
                    f"Public job position not found with slug or ID: {query.slug_or_id}"
                )

        # Verify position is not None and is public
        if job_position is None:
            raise JobPositionNotFoundError(
                f"Public job position not found with slug or ID: {query.slug_or_id}"
            )

        # Check visibility
        if job_position.visibility != JobPositionVisibilityEnum.PUBLIC:
            raise JobPositionNotFoundError(
                f"Job position {query.slug_or_id} is not publicly available"
            )

        return JobPositionDto.from_entity(job_position)
