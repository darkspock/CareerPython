"""Update interview answer command"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.event_bus import EventBus
from src.interview_bc.interview.domain.events.interview_answer_events import InterviewAnswerUpdatedEvent
from src.interview_bc.interview.domain.exceptions.interview_answer_exceptions import InterviewAnswerNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class UpdateInterviewAnswerCommand(Command):
    answer_id: str
    answer_text: Optional[str] = None
    updated_by: Optional[str] = None


class UpdateInterviewAnswerCommandHandler(CommandHandler[UpdateInterviewAnswerCommand]):
    def __init__(self, answer_repository: InterviewAnswerRepositoryInterface, event_bus: EventBus):
        self.answer_repository = answer_repository
        self.event_bus = event_bus

    def execute(self, command: UpdateInterviewAnswerCommand) -> None:
        # Get existing answer
        answer = self.answer_repository.get_by_id(command.answer_id)
        if not answer:
            raise InterviewAnswerNotFoundException(f"Interview answer with id {command.answer_id} not found")

        # Update fields
        if command.answer_text is not None:
            answer.answer_text = command.answer_text
            if not answer.answered_at:
                answer.answered_at = datetime.utcnow()

        answer.updated_at = datetime.utcnow()
        answer.updated_by = command.updated_by

        # Save updated answer
        updated_answer = self.answer_repository.update(answer)

        # Dispatch domain event
        self.event_bus.dispatch(InterviewAnswerUpdatedEvent(
            answer_id=updated_answer.id.value,
            interview_id=updated_answer.interview_id.value,
            question_id=updated_answer.question_id.value,
            answer_text=updated_answer.answer_text,
            updated_at=updated_answer.updated_at or datetime.utcnow(),
            updated_by=command.updated_by
        ))
