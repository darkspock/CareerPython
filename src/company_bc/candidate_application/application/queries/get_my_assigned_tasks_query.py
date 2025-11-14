"""
Get My Assigned Tasks Query
Phase 6: Query to retrieve applications assigned to a user at their current stage
"""

from dataclasses import dataclass
from typing import List, Optional

from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto import \
    CandidateApplicationDto
from src.company_bc.candidate_application.application.queries.shared.candidate_application_dto_mapper import \
    CandidateApplicationDtoMapper
from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import (
    CandidateApplicationRepositoryInterface
)
from src.company_bc.position_stage_assignment.domain.repositories.position_stage_assignment_repository_interface import (
    PositionStageAssignmentRepositoryInterface
)
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetMyAssignedTasksQuery(Query):
    """Query to get applications assigned to a specific user"""
    user_id: str
    stage_id: Optional[str] = None  # Filter by specific stage
    limit: Optional[int] = None


class GetMyAssignedTasksQueryHandler(QueryHandler[GetMyAssignedTasksQuery, List[CandidateApplicationDto]]):
    """Handler for getting user's assigned tasks"""

    def __init__(
            self,
            application_repository: CandidateApplicationRepositoryInterface,
            stage_assignment_repository: PositionStageAssignmentRepositoryInterface
    ):
        self.application_repository = application_repository
        self.stage_assignment_repository = stage_assignment_repository

    def handle(self, query: GetMyAssignedTasksQuery) -> List[CandidateApplicationDto]:
        """Get applications where user is assigned to the current stage

        Returns applications sorted by:
        1. Priority (calculated from deadline and time in stage)
        2. Stage entered time (oldest first)
        """
        # Get all applications
        # TODO: This needs optimization - should be a dedicated repository method
        # For now, we'll get all and filter in memory (not scalable)

        # Get all position-stage assignments where user is assigned
        user_assigned_stages = self._get_user_assigned_stages(query.user_id)

        if not user_assigned_stages:
            return []

        # Get applications that are in those stages
        assigned_applications = []

        for position_id, stage_ids in user_assigned_stages.items():
            # Get all applications for this position
            from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
            applications = self.application_repository.get_applications_by_position(
                JobPositionId(position_id)
            )

            for app in applications:
                # Check if application is in one of the assigned stages
                if app.current_stage_id and app.current_stage_id in stage_ids:
                    # Apply stage filter if provided
                    if query.stage_id is None or app.current_stage_id == query.stage_id:
                        assigned_applications.append(app)

        # Sort by priority (descending) and stage_entered_at (ascending)
        sorted_applications = sorted(
            assigned_applications,
            key=lambda app: (
                -app.calculate_priority().total_score,  # Higher priority first
                app.stage_entered_at or app.applied_at  # Older entries first
            )
        )

        # Apply limit if provided
        if query.limit:
            sorted_applications = sorted_applications[:query.limit]

        # Convert to DTOs
        return [
            CandidateApplicationDtoMapper.from_entity(app)
            for app in sorted_applications
        ]

    def _get_user_assigned_stages(self, user_id: str) -> dict[str, List[str]]:
        """Get all position-stage combinations where user is assigned

        Returns:
            Dict mapping position_id to list of stage_ids where user is assigned
        """
        # Get all assignments where user is assigned
        user_assignments = self.stage_assignment_repository.list_by_user(user_id)

        # Group by position
        user_stages: dict[str, List[str]] = {}

        for assignment in user_assignments:
            position_id = assignment.position_id
            stage_id = assignment.stage_id

            if position_id not in user_stages:
                user_stages[position_id.value] = []

            user_stages[position_id.value].append(stage_id.value)

        return user_stages
