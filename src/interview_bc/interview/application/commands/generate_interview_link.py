"""Generate interview link command"""
import logging
from dataclasses import dataclass
from typing import Optional

from core.event_bus import EventBus
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.framework.application.command_bus import Command, CommandHandler

logger = logging.getLogger(__name__)


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
        token_preview = interview.link_token[:10] if interview.link_token else "None"
        logger.info(f"Generated link token for interview {command.interview_id}: {token_preview}... (expires: {interview.link_expires_at})")

        # Save updated interview
        updated_interview = self.interview_repository.update(interview)
        logger.info(f"Updated interview {command.interview_id}. Token saved: {updated_interview.link_token[:10] if updated_interview.link_token else 'None'}...")

        # Note: We could dispatch an event here if needed, but for now we'll keep it simple

