"""Invite interviewer command"""
from dataclasses import dataclass
from typing import Optional

from core.event_bus import EventBus
from src.interview_bc.interview.domain.entities.interview_interviewer import InterviewInterviewer
from src.interview_bc.interview.domain.exceptions.interview_exceptions import (
    InterviewNotFoundException,
    InterviewPermissionDeniedError
)
from src.interview_bc.interview.domain.infrastructure.interview_interviewer_repository_interface import \
    InterviewInterviewerRepositoryInterface
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview.domain.value_objects.interview_interviewer_id import InterviewInterviewerId
from src.interview_bc.interview.application.services.interview_permission_service import InterviewPermissionService
from src.auth_bc.user.domain.value_objects.UserId import UserId
from src.company_bc.company.domain.value_objects import CompanyId, CompanyUserId
from src.company_bc.company.domain.infrastructure.company_user_repository_interface import CompanyUserRepositoryInterface
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class InviteInterviewerCommand(Command):
    interview_id: str
    user_id: str  # User ID of the interviewer (should have GUEST role for external interviewers)
    company_id: str  # Company ID for permission validation
    name: Optional[str] = None  # Display name (optional, can use user name if not provided)
    is_external: bool = False  # True if interviewer is external (GUEST role)
    invited_by: Optional[str] = None  # User ID who sent the invitation


class InviteInterviewerCommandHandler(CommandHandler[InviteInterviewerCommand]):
    def __init__(
        self,
        interview_repository: InterviewRepositoryInterface,
        interviewer_repository: InterviewInterviewerRepositoryInterface,
        permission_service: InterviewPermissionService,
        company_user_repository: CompanyUserRepositoryInterface,
        event_bus: EventBus
    ):
        self.interview_repository = interview_repository
        self.interviewer_repository = interviewer_repository
        self.permission_service = permission_service
        self.company_user_repository = company_user_repository
        self.event_bus = event_bus

    def execute(self, command: InviteInterviewerCommand) -> None:
        """Invite an interviewer to an interview"""
        # Verify interview exists
        interview = self.interview_repository.get_by_id(command.interview_id)
        if not interview:
            raise InterviewNotFoundException(f"Interview with id {command.interview_id} not found")

        # Validate permissions: user must be able to invite interviewers
        if not command.invited_by:
            raise ValueError("invited_by is required")
        
        if not self.permission_service.can_user_invite_interviewer(
            user_id=command.invited_by,
            company_id=command.company_id,
            interview=interview
        ):
            raise InterviewPermissionDeniedError(
                f"User {command.invited_by} does not have permission to invite interviewers"
            )

        # Check if interviewer is already invited
        existing = self.interviewer_repository.get_by_interview_and_user(
            command.interview_id,
            command.user_id
        )
        if existing:
            raise ValueError(f"User {command.user_id} is already invited as interviewer for this interview")

        # Validate that the user has at least one of the required roles for the interview
        if interview.required_roles:
            # Get the company user to check their roles
            company_user = self.company_user_repository.get_by_company_and_user(
                CompanyId.from_string(command.company_id),
                UserId.from_string(command.user_id)
            )
            
            if not company_user:
                raise ValueError(f"User {command.user_id} is not a member of company {command.company_id}")
            
            # Get the user's assigned company roles
            user_role_ids = self.company_user_repository.get_company_role_ids(company_user.id)
            
            # Check if user has at least one of the required roles
            required_role_ids = [role_id.value for role_id in interview.required_roles]
            has_required_role = any(role_id in user_role_ids for role_id in required_role_ids)
            
            if not has_required_role:
                raise ValueError(
                    f"User {command.user_id} does not have any of the required roles for this interview. "
                    f"Required roles: {required_role_ids}, User roles: {user_role_ids}"
                )

        # Create interviewer relationship
        interviewer_id = InterviewInterviewerId.generate()
        interviewer = InterviewInterviewer.create(
            id=interviewer_id,
            interview_id=InterviewId.from_string(command.interview_id),
            user_id=UserId.from_string(command.user_id),
            name=command.name,
            is_external=command.is_external,
            created_by=command.invited_by
        )

        # Save interviewer relationship
        self.interviewer_repository.create(interviewer)

        # Note: Could dispatch an event here to send invitation email/notification

