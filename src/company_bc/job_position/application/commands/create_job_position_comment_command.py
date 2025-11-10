"""Create Job Position Comment Command."""
from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.job_position.domain.entities.job_position_comment import JobPositionComment
from src.company_bc.job_position.domain.entities.job_position_activity import JobPositionActivity
from src.company_bc.job_position.domain.enums import (
    CommentVisibilityEnum,
    CommentReviewStatusEnum,
)
from src.company_bc.job_position.domain.value_objects import (
    JobPositionCommentId,
    JobPositionId,
    JobPositionWorkflowId,
    JobPositionActivityId,
)
from src.company_bc.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.company_bc.job_position.domain.infrastructure.job_position_activity_repository_interface import (
    JobPositionActivityRepositoryInterface
)
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId


@dataclass(frozen=True)
class CreateJobPositionCommentCommand(Command):
    """
    Command to create a new job position comment
    """
    job_position_id: str
    comment: str
    created_by_user_id: str
    workflow_id: Optional[str] = None
    stage_id: Optional[str] = None  # NULL = global comment
    visibility: str = "private"
    review_status: str = "reviewed"


class CreateJobPositionCommentCommandHandler(CommandHandler[CreateJobPositionCommentCommand]):
    """Handler for CreateJobPositionCommentCommand"""

    def __init__(
        self,
        comment_repository: JobPositionCommentRepositoryInterface,
        activity_repository: JobPositionActivityRepositoryInterface,
    ):
        self._comment_repository = comment_repository
        self._activity_repository = activity_repository

    def execute(self, command: CreateJobPositionCommentCommand) -> None:
        """
        Execute the command
        
        Args:
            command: Command with data for creating the comment
        """
        # Generate ID for the new comment
        comment_id = JobPositionCommentId.generate()
        job_position_id = JobPositionId.from_string(command.job_position_id)
        created_by_user_id = CompanyUserId.from_string(command.created_by_user_id)
        
        # Validate workflow_id exists in job_position_workflows before using it
        # If workflow_id doesn't exist in job_position_workflows, ignore it (set to None)
        workflow_id = None
        if command.workflow_id:
            try:
                # Try to parse as JobPositionWorkflowId
                workflow_id_vo = JobPositionWorkflowId.from_string(command.workflow_id)
                # Verify it exists in job_position_workflows table
                from core.database import SQLAlchemyDatabase
                from src.company_bc.job_position.infrastructure.models.job_position_workflow_model import JobPositionWorkflowModel
                
                database = SQLAlchemyDatabase()
                with database.get_session() as session:
                    workflow_model = session.query(JobPositionWorkflowModel).filter(
                        JobPositionWorkflowModel.id == str(workflow_id_vo)
                    ).first()
                    
                    if workflow_model:
                        workflow_id = workflow_id_vo
                    # If not found, workflow_id remains None (ignore invalid workflow_id)
            except (ValueError, Exception):
                # Invalid workflow_id format or doesn't exist, ignore it
                workflow_id = None

        # Create the comment entity
        comment = JobPositionComment.create(
            id=comment_id,
            job_position_id=job_position_id,
            comment=command.comment,
            created_by_user_id=created_by_user_id,
            workflow_id=workflow_id,
            stage_id=command.stage_id,
            visibility=CommentVisibilityEnum(command.visibility),
            review_status=CommentReviewStatusEnum(command.review_status),
        )

        # Save the comment
        self._comment_repository.save(comment)

        # Create activity log for comment creation
        activity_id = JobPositionActivityId.generate()
        activity = JobPositionActivity.from_comment_added(
            id=activity_id,
            job_position_id=job_position_id,
            user_id=created_by_user_id,
            comment_id=str(comment_id),
            is_global=comment.is_global,
        )

        # Save the activity
        self._activity_repository.save(activity)

