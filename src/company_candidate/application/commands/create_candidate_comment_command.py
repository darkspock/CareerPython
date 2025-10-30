from dataclasses import dataclass
from typing import Optional

from src.shared.application.command_bus import Command, CommandHandler
from src.company_candidate.domain.entities.candidate_comment import CandidateComment
from src.company_candidate.domain.value_objects import CandidateCommentId, CompanyCandidateId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_candidate.domain.enums import CommentVisibility, CommentReviewStatus
from src.company_candidate.domain.infrastructure.candidate_comment_repository_interface import CandidateCommentRepositoryInterface


@dataclass(frozen=True)
class CreateCandidateCommentCommand(Command):
    """Command to create a new candidate comment"""
    id: str
    company_candidate_id: str
    comment: str
    created_by_user_id: str
    workflow_id: Optional[str] = None
    stage_id: Optional[str] = None
    visibility: str = "private"
    review_status: str = "reviewed"


class CreateCandidateCommentCommandHandler(CommandHandler[CreateCandidateCommentCommand]):
    """Handler for creating candidate comments"""

    def __init__(self, repository: CandidateCommentRepositoryInterface):
        self._repository = repository

    def execute(self, command: CreateCandidateCommentCommand) -> None:
        """Handle the create candidate comment command"""
        comment = CandidateComment.create(
            id=CandidateCommentId.from_string(command.id),
            company_candidate_id=CompanyCandidateId.from_string(command.company_candidate_id),
            comment=command.comment,
            created_by_user_id=CompanyUserId.from_string(command.created_by_user_id),
            workflow_id=CompanyWorkflowId.from_string(command.workflow_id) if command.workflow_id else None,
            stage_id=WorkflowStageId.from_string(command.stage_id) if command.stage_id else None,
            visibility=CommentVisibility(command.visibility),
            review_status=CommentReviewStatus(command.review_status),
        )
        
        self._repository.save(comment)

