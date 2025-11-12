"""Accept interviewer invitation command"""
from dataclasses import dataclass
from typing import Optional

from src.interview_bc.interview.domain.exceptions.interview_exceptions import (
    InterviewNotFoundException,
    InterviewPermissionDeniedError
)
from src.interview_bc.interview.domain.infrastructure.interview_interviewer_repository_interface import \
    InterviewInterviewerRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_interviewer_id import InterviewInterviewerId
from src.interview_bc.interview.application.services.interview_permission_service import InterviewPermissionService
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class AcceptInterviewerInvitationCommand(Command):
    interviewer_id: str  # InterviewInterviewer ID
    accepted_by: Optional[str] = None  # User ID who accepted (should match user_id in relationship)


class AcceptInterviewerInvitationCommandHandler(CommandHandler[AcceptInterviewerInvitationCommand]):
    def __init__(
        self,
        interviewer_repository: InterviewInterviewerRepositoryInterface,
        permission_service: InterviewPermissionService
    ):
        self.interviewer_repository = interviewer_repository
        self.permission_service = permission_service

    def execute(self, command: AcceptInterviewerInvitationCommand) -> None:
        """Accept an interviewer invitation"""
        # Get interviewer relationship
        interviewer = self.interviewer_repository.get_by_id(command.interviewer_id)
        if not interviewer:
            raise InterviewNotFoundException(
                f"Interview interviewer relationship with id {command.interviewer_id} not found"
            )

        # Validate permissions: user must be the one invited
        if not command.accepted_by:
            raise ValueError("accepted_by is required")

        if not self.permission_service.can_user_accept_invitation(
            user_id=command.accepted_by,
            interviewer=interviewer
        ):
            raise InterviewPermissionDeniedError(
                f"User {command.accepted_by} does not have permission to accept this invitation"
            )

        # Accept invitation
        interviewer.accept_invitation(accepted_by=command.accepted_by)

        # Update in repository
        self.interviewer_repository.update(interviewer)

