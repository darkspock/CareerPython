"""Job Position Comment Controller."""
from typing import Optional, List

from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.job_position.application.dtos.job_position_comment_dto import JobPositionCommentDto
from src.job_position.application.dtos.job_position_activity_dto import JobPositionActivityDto
from src.job_position.application.commands.create_job_position_comment_command import CreateJobPositionCommentCommand
from src.job_position.application.commands.update_job_position_comment_command import UpdateJobPositionCommentCommand
from src.job_position.application.commands.delete_job_position_comment_command import DeleteJobPositionCommentCommand
from src.job_position.application.commands.mark_comment_as_reviewed_command import MarkJobPositionCommentAsReviewedCommand
from src.job_position.application.commands.mark_comment_as_pending_command import MarkJobPositionCommentAsPendingCommand
from src.job_position.application.queries.list_job_position_comments_query import ListJobPositionCommentsQuery
from src.job_position.application.queries.list_job_position_activities_query import ListJobPositionActivitiesQuery
from adapters.http.admin.schemas.job_position_comment import (
    CreateJobPositionCommentRequest,
    UpdateJobPositionCommentRequest,
    JobPositionCommentResponse,
    JobPositionCommentListResponse,
)
from adapters.http.admin.schemas.job_position_activity import (
    JobPositionActivityResponse,
    JobPositionActivityListResponse,
)


class JobPositionCommentController:
    """Controller for job position comment operations"""

    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus,
    ):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_comment(
        self,
        job_position_id: str,
        request: CreateJobPositionCommentRequest,
        user_id: str,
    ) -> None:
        """
        Create a new comment for a job position
        
        Args:
            job_position_id: ID of the job position
            request: Request with comment data
            user_id: ID of the user creating the comment
        """
        command = CreateJobPositionCommentCommand(
            job_position_id=job_position_id,
            comment=request.comment,
            created_by_user_id=user_id,
            workflow_id=request.workflow_id,
            stage_id=request.stage_id,
            visibility=request.visibility.value,
            review_status=request.review_status.value,
        )
        
        self._command_bus.dispatch(command)

    def update_comment(
        self,
        comment_id: str,
        request: UpdateJobPositionCommentRequest,
    ) -> None:
        """
        Update an existing comment
        
        Args:
            comment_id: ID of the comment to update
            request: Request with updated data
        """
        command = UpdateJobPositionCommentCommand(
            comment_id=comment_id,
            comment=request.comment,
            visibility=request.visibility.value if request.visibility else None,
        )
        
        self._command_bus.dispatch(command)

    def delete_comment(self, comment_id: str) -> None:
        """
        Delete a comment
        
        Args:
            comment_id: ID of the comment to delete
        """
        command = DeleteJobPositionCommentCommand(
            comment_id=comment_id,
        )
        
        self._command_bus.dispatch(command)

    def mark_comment_as_reviewed(self, comment_id: str) -> None:
        """
        Mark a comment as reviewed
        
        Args:
            comment_id: ID of the comment to mark as reviewed
        """
        command = MarkJobPositionCommentAsReviewedCommand(
            comment_id=comment_id,
        )
        
        self._command_bus.dispatch(command)

    def mark_comment_as_pending(self, comment_id: str) -> None:
        """
        Mark a comment as pending
        
        Args:
            comment_id: ID of the comment to mark as pending
        """
        command = MarkJobPositionCommentAsPendingCommand(
            comment_id=comment_id,
        )
        
        self._command_bus.dispatch(command)

    def list_comments(
        self,
        job_position_id: str,
        stage_id: Optional[str] = None,
        include_global: bool = True,
    ) -> JobPositionCommentListResponse:
        """
        List comments for a job position
        
        Args:
            job_position_id: ID of the job position
            stage_id: Optional stage ID to filter by
            include_global: Include global comments (default: True)
            
        Returns:
            JobPositionCommentListResponse: List of comments
        """
        query = ListJobPositionCommentsQuery(
            job_position_id=job_position_id,
            stage_id=stage_id,
            include_global=include_global,
        )
        
        comment_dtos: List[JobPositionCommentDto] = self._query_bus.query(query)
        
        return JobPositionCommentListResponse(
            items=[
                JobPositionCommentResponse(**dto.__dict__)
                for dto in comment_dtos
            ],
            total=len(comment_dtos),
        )

    def list_activities(
        self,
        job_position_id: str,
        limit: int = 50,
    ) -> JobPositionActivityListResponse:
        """
        List activities for a job position
        
        Args:
            job_position_id: ID of the job position
            limit: Maximum number of activities to return
            
        Returns:
            JobPositionActivityListResponse: List of activities
        """
        query = ListJobPositionActivitiesQuery(
            job_position_id=job_position_id,
            limit=limit,
        )
        
        activity_dtos: List[JobPositionActivityDto] = self._query_bus.query(query)
        
        return JobPositionActivityListResponse(
            items=[
                JobPositionActivityResponse(**dto.__dict__)
                for dto in activity_dtos
            ],
            total=len(activity_dtos),
        )

