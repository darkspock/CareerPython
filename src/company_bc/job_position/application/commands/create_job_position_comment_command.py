"""Create Job Position Comment Command."""
from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.job_position.domain.entities.job_position_activity import JobPositionActivity
from src.company_bc.job_position.domain.entities.job_position_comment import JobPositionComment
from src.company_bc.job_position.domain.enums import (
    CommentVisibilityEnum,
    CommentReviewStatusEnum,
)
from src.company_bc.job_position.domain.infrastructure.job_position_activity_repository_interface import (
    JobPositionActivityRepositoryInterface
)
from src.company_bc.job_position.domain.infrastructure.job_position_comment_repository_interface import (
    JobPositionCommentRepositoryInterface
)
from src.company_bc.job_position.domain.value_objects import (
    JobPositionCommentId,
    JobPositionId,
    JobPositionWorkflowId,
    JobPositionActivityId,
)
from src.framework.application.command_bus import Command, CommandHandler
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


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
            workflow_repository: WorkflowRepositoryInterface,
    ):
        self._comment_repository = comment_repository
        self._activity_repository = activity_repository
        self._workflow_repository = workflow_repository

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

        # Validate workflow_id exists in shared workflows system before using it
        # If workflow_id doesn't exist, ignore it (set to None)
        workflow_id = None
        if command.workflow_id:
            try:
                # Convert to WorkflowId and verify it exists in shared workflows table
                workflow_id_shared = WorkflowId.from_string(command.workflow_id)
                workflow = self._workflow_repository.get_by_id(workflow_id_shared)

                if workflow:
                    # Convert back to JobPositionWorkflowId for the comment entity
                    workflow_id = JobPositionWorkflowId.from_string(command.workflow_id)
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
