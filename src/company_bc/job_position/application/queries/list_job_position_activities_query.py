"""List Job Position Activities Query."""
from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.domain.infrastructure.job_position_activity_repository_interface import (
    JobPositionActivityRepositoryInterface
)
from src.company_bc.job_position.application.dtos.job_position_activity_dto import JobPositionActivityDto


@dataclass(frozen=True)
class ListJobPositionActivitiesQuery(Query):
    """
    Query to list activities for a job position
    """
    job_position_id: str
    limit: int = 50


class ListJobPositionActivitiesQueryHandler(QueryHandler[ListJobPositionActivitiesQuery, List[JobPositionActivityDto]]):
    """Handler for ListJobPositionActivitiesQuery"""

    def __init__(self, activity_repository: JobPositionActivityRepositoryInterface):
        self._repository = activity_repository

    def handle(self, query: ListJobPositionActivitiesQuery) -> List[JobPositionActivityDto]:
        """
        Execute the query
        
        Args:
            query: Query with filters
            
        Returns:
            List[JobPositionActivityDto]: List of activities
        """
        job_position_id = JobPositionId.from_string(query.job_position_id)
        
        # Retrieve activities
        activities = self._repository.list_by_job_position(
            job_position_id,
            query.limit
        )

        # Convert to DTOs
        return [
            JobPositionActivityDto(
                id=str(activity.id),
                job_position_id=str(activity.job_position_id),
                activity_type=activity.activity_type.value,
                description=activity.description,
                performed_by_user_id=str(activity.performed_by_user_id),
                metadata=activity.metadata,
                created_at=activity.created_at,
            )
            for activity in activities
        ]

