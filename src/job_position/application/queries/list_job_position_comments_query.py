"""List Job Position Comments Query."""
from dataclasses import dataclass
from typing import Optional, List

from src.shared.application.query_bus import Query, QueryHandler
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.job_position.application.dtos.job_position_comment_dto import JobPositionCommentDto


@dataclass(frozen=True)
class ListJobPositionCommentsQuery(Query):
    """
    Query to list comments for a job position
    
    Can be filtered by:
    - All comments (stage_id = None, include_global = None)
    - Comments for specific stage + global (stage_id = value, include_global = True)
    - Only global comments (stage_id = None, include_global = True via list_global_only)
    """
    job_position_id: str
    stage_id: Optional[str] = None  # Specific stage, or None
    include_global: bool = True  # Include global comments (stage_id IS NULL)


class ListJobPositionCommentsQueryHandler(QueryHandler[ListJobPositionCommentsQuery, List[JobPositionCommentDto]]):
    """Handler for ListJobPositionCommentsQuery"""

    def __init__(self, comment_repository: JobPositionCommentRepositoryInterface):
        self._repository = comment_repository

    def handle(self, query: ListJobPositionCommentsQuery) -> List[JobPositionCommentDto]:
        """
        Execute the query
        
        Args:
            query: Query with filters
            
        Returns:
            List[JobPositionCommentDto]: List of comments
        """
        job_position_id = JobPositionId.from_string(query.job_position_id)
        
        # Use the repository method that handles stage and global filtering
        comments = self._repository.list_by_stage_and_global(
            job_position_id=job_position_id,
            stage_id=query.stage_id,
            include_global=query.include_global
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
                review_status=comment.review_status,
                visibility=comment.visibility,
                created_at=comment.created_at,
                updated_at=comment.updated_at,
            )
            for comment in comments
        ]

