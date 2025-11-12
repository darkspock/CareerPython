"""Generate interview link command"""
from dataclasses import dataclass
from typing import Optional

from core.event_bus import EventBus
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class GenerateInterviewLinkCommand(Command):
    interview_id: str
    expires_in_days: int = 30  # Default expiration: 30 days
    generated_by: Optional[str] = None


class GenerateInterviewLinkCommandHandler(CommandHandler[GenerateInterviewLinkCommand]):
    def __init__(self, interview_repository: InterviewRepositoryInterface, event_bus: EventBus):
        self.interview_repository = interview_repository
        self.event_bus = event_bus

    def execute(self, command: GenerateInterviewLinkCommand) -> None:
        # Get existing interview
        interview = self.interview_repository.get_by_id(command.interview_id)
        
        if not interview:
            raise InterviewNotFoundException(f"Interview with id {command.interview_id} not found")

        # Generate link token
        interview.generate_link_token(expires_in_days=command.expires_in_days)

        # Save updated interview
        self.interview_repository.update(interview)

        # Note: We could dispatch an event here if needed, but for now we'll keep it simple

