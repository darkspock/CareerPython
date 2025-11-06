"""List All Job Position Comments Query."""
from dataclasses import dataclass
from typing import List, Optional

from src.job_position.application.dtos.job_position_comment_dto import JobPositionCommentDto
from src.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.job_position.domain.value_objects import JobPositionId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListAllJobPositionCommentsQuery(Query):
    """
    Query to list ALL comments for a job position (no stage filtering, but with visibility filtering)
    """
    job_position_id: str
    current_user_id: Optional[str] = None  # For visibility filtering


class ListAllJobPositionCommentsQueryHandler(
    QueryHandler[ListAllJobPositionCommentsQuery, List[JobPositionCommentDto]]):
    """Handler for ListAllJobPositionCommentsQuery"""

    def __init__(self, comment_repository: JobPositionCommentRepositoryInterface):
        self._repository = comment_repository

    def handle(self, query: ListAllJobPositionCommentsQuery) -> List[JobPositionCommentDto]:
        """
        Execute the query

        Args:
            query: Query with job position ID

        Returns:
            List[JobPositionCommentDto]: List of ALL comments
        """
        job_position_id = JobPositionId.from_string(query.job_position_id)

        # Use the repository method that returns ALL comments (with visibility filtering)
        comments = self._repository.list_by_job_position(
            job_position_id,
            current_user_id=query.current_user_id
        )

        # Convert to DTOs
        return [
            JobPositionCommentDto(
                id=str(comment.id),
                job_position_id=str(comment.job_position_id),
                comment=comment.comment,
                workflow_id=str(comment.workflow_id) if comment.workflow_id else None,
                stage_id=comment.stage_id,
                created_by_user_id=str(comment.created_by_user_id),
                review_status=comment.review_status.value,
                visibility=comment.visibility.value,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
                is_global=comment.is_global,
            )
            for comment in comments
        ]
