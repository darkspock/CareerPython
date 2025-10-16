from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.exceptions.interview_exceptions import \
    InterviewTemplateQuestionNotFoundException
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.shared.application.command_bus import Command


@dataclass
class EnableInterviewTemplateQuestionCommand(Command):
    question_id: InterviewTemplateQuestionId
    enabled_by: str
    enable_reason: Optional[str] = None


class EnableInterviewTemplateQuestionCommandHandler:
    def __init__(
            self,
            question_repository: InterviewTemplateQuestionRepository
    ):
        self.question_repository = question_repository

    def execute(self, command: EnableInterviewTemplateQuestionCommand) -> None:
        """Enable a previously disabled interview template question"""

        # Get the question
        question = self.question_repository.get_by_id(command.question_id)
        if not question:
            raise InterviewTemplateQuestionNotFoundException(f"Question with id {command.question_id} not found")

        # Enable the question using the entity method
        question.enable()
        self.question_repository.update_entity(question)
