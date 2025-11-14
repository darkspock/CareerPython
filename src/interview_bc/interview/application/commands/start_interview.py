"""Start interview command"""
from dataclasses import dataclass
from datetime import datetime

from core.event_bus import EventBus
from src.framework.application.command_bus import Command, CommandHandler
from src.interview_bc.interview.domain.events.interview_events import InterviewStartedEvent
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface


@dataclass
class StartInterviewCommand(Command):
    interview_id: str
    started_by: str


class StartInterviewCommandHandler(CommandHandler[StartInterviewCommand]):
    def __init__(self, interview_repository: InterviewRepositoryInterface, event_bus: EventBus):
        self.interview_repository = interview_repository
        self.event_bus = event_bus

    def execute(self, command: StartInterviewCommand) -> None:
        # Get existing interview
        interview = self.interview_repository.get_by_id(command.interview_id)
        if not interview:
            raise InterviewNotFoundException(f"Interview with id {command.interview_id} not found")

        # Start the interview
        interview.start(started_by=command.started_by)

        # Save updated interview
        updated_interview = self.interview_repository.update(interview)

        # Dispatch domain event
        self.event_bus.dispatch(InterviewStartedEvent(
            interview_id=updated_interview.id.value,
            candidate_id=updated_interview.candidate_id.value,
            started_at=updated_interview.started_at or datetime.utcnow(),
            started_by=command.started_by
        ))
