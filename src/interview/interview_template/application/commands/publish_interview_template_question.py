from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.enums.interview_template_question import \
    InterviewTemplateQuestionStatusEnum
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateQuestionNotFoundException,
    InvalidTemplateStateException
)
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.shared.application.command_bus import Command


@dataclass
class PublishInterviewTemplateQuestionCommand(Command):
    question_id: InterviewTemplateQuestionId
    published_by: str
    publish_reason: Optional[str] = None


class PublishInterviewTemplateQuestionCommandHandler:
    def __init__(
            self,
            question_repository: InterviewTemplateQuestionRepository
    ):
        self.question_repository = question_repository

    def execute(self, command: PublishInterviewTemplateQuestionCommand) -> None:
        """Publish a question (DRAFT → ENABLED)"""

        # Get the question
        question = self.question_repository.get_by_id(command.question_id)
        if not question:
            raise InterviewTemplateQuestionNotFoundException(f"Question with id {command.question_id.value} not found")

        # Validate that question can be published
        if question.status != InterviewTemplateQuestionStatusEnum.DRAFT:
            raise InvalidTemplateStateException(
                f"Question {command.question_id.value} must be in DRAFT status to be published. Current status: {question.status.value}"
            )

        # Publish the question by setting status to ENABLED
        question.status = InterviewTemplateQuestionStatusEnum.ENABLED
        self.question_repository.update_entity(question)
