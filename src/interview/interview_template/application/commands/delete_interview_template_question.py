from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateQuestionNotFoundException
)
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.shared.application.command_bus import Command


@dataclass
class DeleteInterviewTemplateQuestionCommand(Command):
    question_id: InterviewTemplateQuestionId
    deleted_by: str
    delete_reason: Optional[str] = None


class DeleteInterviewTemplateQuestionCommandHandler:
    def __init__(
            self,
            question_repository: InterviewTemplateQuestionRepository
    ):
        self.question_repository = question_repository

    def execute(self, command: DeleteInterviewTemplateQuestionCommand) -> None:
        """Delete an interview template question"""

        # Get the question
        question = self.question_repository.get_by_id(command.question_id)
        if not question:
            raise InterviewTemplateQuestionNotFoundException(f"Question with id {command.question_id.value} not found")

        self.question_repository.delete(question.id)
