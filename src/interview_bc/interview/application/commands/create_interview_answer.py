"""Create interview answer command"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from core.event_bus import EventBus
from src.framework.application.command_bus import Command, CommandHandler
from src.interview_bc.interview.domain.entities.interview_answer import InterviewAnswer
from src.interview_bc.interview.domain.events.interview_answer_events import InterviewAnswerCreatedEvent
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_answer_id import InterviewAnswerId
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId


@dataclass
class CreateInterviewAnswerCommand(Command):
    interview_id: str
    question_id: str
    question_text: Optional[str] = None
    answer_text: Optional[str] = None
    created_by: Optional[str] = None


class CreateInterviewAnswerCommandHandler(CommandHandler[CreateInterviewAnswerCommand]):
    def __init__(self, answer_repository: InterviewAnswerRepositoryInterface, event_bus: EventBus):
        self.answer_repository = answer_repository
        self.event_bus = event_bus

    def execute(self, command: CreateInterviewAnswerCommand) -> None:
        # Generate new answer ID
        answer_id = InterviewAnswerId.generate()

        # Convert string IDs to value objects
        interview_id = InterviewId.from_string(command.interview_id)
        question_id = InterviewTemplateQuestionId.from_string(command.question_id)

        # Create answer entity
        new_answer = InterviewAnswer(
            id=answer_id,
            interview_id=interview_id,
            question_id=question_id,
            question_text=command.question_text,
            answer_text=command.answer_text,
            answered_at=datetime.utcnow() if command.answer_text else None,
            created_by=command.created_by
        )

        # Save answer
        created_answer = self.answer_repository.create(new_answer)

        # Dispatch domain event
        if created_answer.answered_at:
            self.event_bus.dispatch(InterviewAnswerCreatedEvent(
                answer_id=created_answer.id.value,
                interview_id=created_answer.interview_id.value,
                question_id=created_answer.question_id.value,
                answer_text=created_answer.answer_text,
                answered_at=created_answer.answered_at,
                created_by=created_answer.created_by
            ))
