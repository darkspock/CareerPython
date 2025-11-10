"""Create interview command"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from core.event_bus import EventBus
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.value_objects import CandidateApplicationId
from src.interview_bc.interview.domain.entities.interview import Interview
from src.interview_bc.interview.domain.enums.interview_enums import InterviewTypeEnum
from src.interview_bc.interview.domain.events.interview_events import InterviewCreatedEvent
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class CreateInterviewCommand(Command):
    candidate_id: str
    interview_type: str = InterviewTypeEnum.JOB_POSITION.value
    job_position_id: Optional[str] = None
    application_id: Optional[str] = None
    interview_template_id: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[str] = None  # ISO datetime string
    interviewers: Optional[List[str]] = None
    created_by: Optional[str] = None


class CreateInterviewCommandHandler(CommandHandler[CreateInterviewCommand]):
    def __init__(self, interview_repository: InterviewRepositoryInterface, event_bus: EventBus):
        self.interview_repository = interview_repository
        self.event_bus = event_bus

    def execute(self, command: CreateInterviewCommand) -> None:
        # Generate new interview ID
        interview_id = InterviewId.generate()

        # Convert string IDs to value objects
        candidate_id = CandidateId.from_string(command.candidate_id)

        job_position_id = None
        if command.job_position_id:
            job_position_id = JobPositionId.from_string(command.job_position_id)

        application_id = None
        if command.application_id:
            application_id = CandidateApplicationId.from_string(command.application_id)

        interview_template_id = None
        if command.interview_template_id:
            interview_template_id = InterviewTemplateId.from_string(command.interview_template_id)

        # Convert interview type
        interview_type = InterviewTypeEnum(command.interview_type)

        # Parse scheduled datetime
        scheduled_at = None
        if command.scheduled_at:
            scheduled_at = datetime.fromisoformat(command.scheduled_at.replace('Z', '+00:00'))

        # Create interview using factory method
        new_interview = Interview.create(
            id=interview_id,
            candidate_id=candidate_id,
            interview_type=interview_type,
            job_position_id=job_position_id,
            application_id=application_id,
            interview_template_id=interview_template_id,
            title=command.title,
            description=command.description,
            scheduled_at=scheduled_at,
            created_by=command.created_by
        )

        # Set interviewers if provided
        if command.interviewers:
            new_interview.interviewers = command.interviewers

        # Save interview
        created_interview = self.interview_repository.create(new_interview)

        # Dispatch domain event
        self.event_bus.dispatch(InterviewCreatedEvent(
            interview_id=created_interview.id.value,
            candidate_id=created_interview.candidate_id.value,
            job_position_id=created_interview.job_position_id.value if created_interview.job_position_id else None,
            interview_template_id=created_interview.interview_template_id.value if created_interview.interview_template_id else None,
            interview_type=created_interview.interview_type.value,
            created_at=created_interview.created_at or datetime.utcnow()
        ))
