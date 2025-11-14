from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any

from src.interview_bc.interview_template.domain.enums import (
    InterviewTemplateQuestionDataTypeEnum,
    InterviewTemplateQuestionScopeEnum
)
from src.interview_bc.interview_template.domain.exceptions.interview_exceptions import (
    InterviewTemplateNotFoundException
)
from src.interview_bc.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview_bc.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview_bc.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.framework.application.command_bus import Command


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
    allow_ai_followup: Optional[bool] = None
    legal_notice: Optional[str] = None
    scoring_values: Optional[List[Dict[str, Any]]] = None
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
            allow_ai_followup=command.allow_ai_followup if command.allow_ai_followup is not None else question.allow_ai_followup,
            legal_notice=command.legal_notice if command.legal_notice is not None else question.legal_notice,
            scoring_values=command.scoring_values if command.scoring_values is not None else question.scoring_values
        )

        self.question_repository.update(question)
