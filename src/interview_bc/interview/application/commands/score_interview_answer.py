"""Score interview answer command"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.event_bus import EventBus
from src.interview.interview.domain.events.interview_answer_events import InterviewAnswerScoredEvent
from src.interview.interview.domain.exceptions.interview_answer_exceptions import InterviewAnswerNotFoundException, \
    InterviewAnswerInvalidScoreException
from src.interview.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class ScoreInterviewAnswerCommand(Command):
    answer_id: str
    score: float
    feedback: Optional[str] = None
    scored_by: Optional[str] = None


class ScoreInterviewAnswerCommandHandler(CommandHandler[ScoreInterviewAnswerCommand]):
    def __init__(self, answer_repository: InterviewAnswerRepositoryInterface, event_bus: EventBus):
        self.answer_repository = answer_repository
        self.event_bus = event_bus

    def execute(self, command: ScoreInterviewAnswerCommand) -> None:
        # Get existing answer
        answer = self.answer_repository.get_by_id(command.answer_id)
        if not answer:
            raise InterviewAnswerNotFoundException(f"Interview answer with id {command.answer_id} not found")

        # Validate score
        if command.score < 0 or command.score > 100:
            raise InterviewAnswerInvalidScoreException(f"Score must be between 0 and 100, got {command.score}")

        # Update scoring fields
        answer.score = command.score
        answer.feedback = command.feedback
        answer.scored_at = datetime.utcnow()
        answer.scored_by = command.scored_by
        answer.updated_at = datetime.utcnow()
        answer.updated_by = command.scored_by

        # Save updated answer
        updated_answer = self.answer_repository.update(answer)

        # Dispatch domain event
        self.event_bus.dispatch(InterviewAnswerScoredEvent(
            answer_id=updated_answer.id.value,
            interview_id=updated_answer.interview_id.value,
            question_id=updated_answer.question_id.value,
            score=updated_answer.score,
            feedback=updated_answer.feedback,
            scored_at=updated_answer.scored_at or datetime.utcnow(),
            scored_by=command.scored_by
        ))
