"""Update interview command"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from core.event_bus import EventBus
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewTypeEnum,
    InterviewProcessTypeEnum,
    InterviewModeEnum
)
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class UpdateInterviewCommand(Command):
    """Command to update an interview"""
    interview_id: str
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[str] = None  # ISO datetime string
    deadline_date: Optional[str] = None  # ISO datetime string
    process_type: Optional[str] = None  # InterviewProcessTypeEnum value
    interview_type: Optional[str] = None  # InterviewTypeEnum value
    interview_mode: Optional[str] = None  # InterviewModeEnum value
    required_roles: Optional[List[str]] = None  # List of CompanyRole IDs
    interviewers: Optional[List[str]] = None  # List of interviewer names/IDs
    interviewer_notes: Optional[str] = None
    feedback: Optional[str] = None
    score: Optional[float] = None
    updated_by: Optional[str] = None


class UpdateInterviewCommandHandler(CommandHandler[UpdateInterviewCommand]):
    def __init__(self, interview_repository: InterviewRepositoryInterface, event_bus: EventBus):
        self.interview_repository = interview_repository
        self.event_bus = event_bus

    def execute(self, command: UpdateInterviewCommand) -> None:
        """Update an interview"""
        # Get existing interview
        interview = self.interview_repository.get_by_id(command.interview_id)
        if not interview:
            raise InterviewNotFoundException(f"Interview with id {command.interview_id} not found")

        # Update basic details
        process_type_enum = None
        if command.process_type:
            process_type_enum = InterviewProcessTypeEnum(command.process_type)

        interview_type_enum = None
        if command.interview_type:
            interview_type_enum = InterviewTypeEnum(command.interview_type)

        interview_mode_enum = None
        if command.interview_mode:
            interview_mode_enum = InterviewModeEnum(command.interview_mode)

        # Parse scheduled datetime if provided
        scheduled_at_datetime = None
        if command.scheduled_at:
            scheduled_at_datetime = datetime.fromisoformat(command.scheduled_at.replace('Z', '+00:00'))

        # Parse deadline datetime if provided
        deadline_date_datetime = None
        if command.deadline_date:
            deadline_date_datetime = datetime.fromisoformat(command.deadline_date.replace('Z', '+00:00'))

        # Update details using entity method
        interview.update_details(
            title=command.title,
            description=command.description,
            process_type=process_type_enum,
            interview_type=interview_type_enum,
            interview_mode=interview_mode_enum,
            deadline_date=deadline_date_datetime,
            updated_by=command.updated_by
        )

        # Update scheduled_at using schedule method if provided
        if scheduled_at_datetime:
            interview.schedule(scheduled_at_datetime, scheduled_by=command.updated_by)

        # Update required roles if provided
        if command.required_roles is not None:
            if not command.required_roles:
                raise ValueError("Required roles cannot be empty")
            required_roles = [CompanyRoleId.from_string(role_id) for role_id in command.required_roles]
            interview.update_required_roles(required_roles, updated_by=command.updated_by)

        # Update interviewers if provided
        if command.interviewers is not None:
            interview.interviewers = command.interviewers

        # Update interviewer notes if provided
        if command.interviewer_notes is not None:
            interview.add_interviewer_notes(command.interviewer_notes, added_by=command.updated_by)

        # Update feedback if provided
        if command.feedback is not None:
            interview.add_feedback(command.feedback, added_by=command.updated_by)

        # Update score if provided
        if command.score is not None:
            interview.set_score(command.score, scored_by=command.updated_by)

        # Save updated interview
        self.interview_repository.update(interview)

        # Note: Could dispatch an event here if needed

