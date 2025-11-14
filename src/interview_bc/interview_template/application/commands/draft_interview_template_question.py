from dataclasses import dataclass
from typing import Optional

from src.framework.application.command_bus import Command
from src.interview_bc.interview_template.domain.enums.interview_template_question import \
    InterviewTemplateQuestionStatusEnum
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateQuestionNotFoundException,
    InvalidTemplateStateException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository


@dataclass
class DraftInterviewTemplateQuestionCommand(Command):
    question_id: InterviewTemplateQuestionId
    drafted_by: str
    draft_reason: Optional[str] = None


class DraftInterviewTemplateQuestionCommandHandler:
    def __init__(
            self,
            question_repository: InterviewTemplateQuestionRepository
    ):
        self.question_repository = question_repository

    def execute(self, command: DraftInterviewTemplateQuestionCommand) -> None:
        """Move question back to draft (ENABLED/DISABLED → DRAFT)"""

        # Get the question
        question = self.question_repository.get_by_id(command.question_id)
        if not question:
            raise InterviewTemplateQuestionNotFoundException(f"Question with id {command.question_id.value} not found")

        # Validate that question can be drafted
        if question.status == InterviewTemplateQuestionStatusEnum.DRAFT:
            raise InvalidTemplateStateException(
                f"Question {command.question_id.value} is already in DRAFT status"
            )

        # Draft the question by setting status to DRAFT
        question.status = InterviewTemplateQuestionStatusEnum.DRAFT
        self.question_repository.update_entity(question)
