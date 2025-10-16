"""Finish interview command"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.event_bus import EventBus
from src.interview.interview.domain.events.interview_events import InterviewFinishedEvent
from src.interview.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class FinishInterviewCommand(Command):
    interview_id: str
    finished_by: str
    score: Optional[float] = None
    feedback: Optional[str] = None
    interviewer_notes: Optional[str] = None


class FinishInterviewCommandHandler(CommandHandler[FinishInterviewCommand]):
    def __init__(self, interview_repository: InterviewRepositoryInterface, event_bus: EventBus):
        self.interview_repository = interview_repository
        self.event_bus = event_bus

    def execute(self, command: FinishInterviewCommand) -> None:
        # Get existing interview
        interview = self.interview_repository.get_by_id(command.interview_id)
        if not interview:
            raise InterviewNotFoundException(f"Interview with id {command.interview_id} not found")

        # Set optional data before finishing
        if command.score is not None:
            interview.set_score(command.score, scored_by=command.finished_by)

        if command.feedback:
            interview.add_feedback(command.feedback, added_by=command.finished_by)

        if command.interviewer_notes:
            interview.add_interviewer_notes(command.interviewer_notes, added_by=command.finished_by)

        # Finish the interview
        interview.finish(finished_by=command.finished_by)

        # Save updated interview
        updated_interview = self.interview_repository.update(interview)

        # Dispatch domain event
        self.event_bus.dispatch(InterviewFinishedEvent(
            interview_id=updated_interview.id.value,
            candidate_id=updated_interview.candidate_id.value,
            finished_at=updated_interview.finished_at or datetime.utcnow(),
            duration_minutes=updated_interview.duration_minutes,
            score=updated_interview.score,
            finished_by=command.finished_by
        ))
