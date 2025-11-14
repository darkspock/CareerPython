"""Submit interview answer by token command"""
from dataclasses import dataclass
from typing import Optional

from core.event_bus import EventBus
from src.interview_bc.interview.domain.entities.interview_answer import InterviewAnswer
from src.interview_bc.interview.domain.events.interview_answer_events import InterviewAnswerCreatedEvent, InterviewAnswerUpdatedEvent
from src.interview_bc.interview.domain.exceptions.interview_exceptions import InterviewNotFoundException
from src.interview_bc.interview.domain.exceptions.interview_answer_exceptions import InterviewAnswerNotFoundException
from src.interview_bc.interview.domain.infrastructure.interview_answer_repository_interface import \
    InterviewAnswerRepositoryInterface
from src.interview_bc.interview.domain.infrastructure.interview_repository_interface import InterviewRepositoryInterface
from src.interview_bc.interview.domain.value_objects.interview_answer_id import InterviewAnswerId
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.framework.application.command_bus import Command, CommandHandler
from datetime import datetime


@dataclass
class SubmitInterviewAnswerByTokenCommand(Command):
    interview_id: str
    token: str
    question_id: str
    answer_text: Optional[str] = None
    question_text: Optional[str] = None


class SubmitInterviewAnswerByTokenCommandHandler(CommandHandler[SubmitInterviewAnswerByTokenCommand]):
    def __init__(
        self,
        interview_repository: InterviewRepositoryInterface,
        answer_repository: InterviewAnswerRepositoryInterface,
        event_bus: EventBus
    ):
        self.interview_repository = interview_repository
        self.answer_repository = answer_repository
        self.event_bus = event_bus

    def execute(self, command: SubmitInterviewAnswerByTokenCommand) -> None:
        # Validate token and get interview
        interview = self.interview_repository.get_by_token(command.interview_id, command.token)
        if not interview:
            raise InterviewNotFoundException(
                f"Interview with id {command.interview_id} not found or token is invalid/expired"
            )

        # Convert string IDs to value objects
        interview_id = InterviewId.from_string(command.interview_id)
        question_id = InterviewTemplateQuestionId.from_string(command.question_id)

        # Check if answer already exists
        existing_answer = self.answer_repository.get_by_interview_and_question(
            command.interview_id,
            command.question_id
        )

        if existing_answer:
            # Update existing answer
            existing_answer.answer_text = command.answer_text
            if not existing_answer.answered_at:
                existing_answer.answered_at = datetime.utcnow()
            existing_answer.updated_at = datetime.utcnow()

            updated_answer = self.answer_repository.update(existing_answer)

            # Dispatch domain event
            self.event_bus.dispatch(InterviewAnswerUpdatedEvent(
                answer_id=updated_answer.id.value,
                interview_id=updated_answer.interview_id.value,
                question_id=updated_answer.question_id.value,
                answer_text=updated_answer.answer_text,
                updated_at=updated_answer.updated_at or datetime.utcnow(),
                updated_by=None
            ))
        else:
            # Create new answer
            answer_id = InterviewAnswerId.generate()

            new_answer = InterviewAnswer(
                id=answer_id,
                interview_id=interview_id,
                question_id=question_id,
                question_text=command.question_text,
                answer_text=command.answer_text,
                answered_at=datetime.utcnow() if command.answer_text else None,
                created_by=None
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

