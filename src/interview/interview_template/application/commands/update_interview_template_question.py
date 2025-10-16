from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.enums import (
    InterviewTemplateQuestionDataTypeEnum,
    InterviewTemplateQuestionScopeEnum
)
from src.interview.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.shared.application.command_bus import Command


@dataclass
class UpdateInterviewTemplateQuestionCommand(Command):
    question_id: InterviewTemplateQuestionId
    interview_template_section_id: InterviewTemplateSectionId
    name: str
    description: str
    data_type: InterviewTemplateQuestionDataTypeEnum
    scope: InterviewTemplateQuestionScopeEnum
    code: str
    sort_order: int
    updated_by: Optional[str] = None


class UpdateInterviewTemplateQuestionCommandHandler:
    def __init__(self, question_repository: InterviewTemplateQuestionRepository):
        self.question_repository = question_repository

    def execute(self, command: UpdateInterviewTemplateQuestionCommand) -> None:
        """Update an existing interview template question"""

        # Get the existing question
        question = self.question_repository.get_by_id(command.question_id)
        if not question:
            raise InterviewTemplateNotFoundException(f"Question with id {command.question_id.value} not found")

        question.update_details(
            interview_template_section_id=command.interview_template_section_id,
            sort_order=command.sort_order,
            name=command.name,
            data_type=command.data_type,
            scope=command.scope,
            code=command.code,
            description=command.description,
        )

        self.question_repository.update(question)
