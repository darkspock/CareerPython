from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.entities.interview_template_question import InterviewTemplateQuestion
from src.interview.interview_template.domain.enums.interview_template_question import \
    InterviewTemplateQuestionScopeEnum, InterviewTemplateQuestionDataTypeEnum
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId
from src.interview.interview_template.infrastructure.repositories.interview_template_question_repository import \
    InterviewTemplateQuestionRepository
from src.shared.application.command_bus import Command


@dataclass
class CreateInterviewTemplateQuestionCommand(Command):
    id: InterviewTemplateQuestionId
    interview_template_section_id: InterviewTemplateSectionId
    scope: InterviewTemplateQuestionScopeEnum
    sort_order: int
    name: str
    description: str
    code: str
    data_type: InterviewTemplateQuestionDataTypeEnum
    allow_ai_followup: bool = False
    legal_notice: Optional[str] = None


class CreateInterviewTemplateQuestionCommandHandler:
    def __init__(self, interview_template_question_repository: InterviewTemplateQuestionRepository):
        self.interview_template_question_repository = interview_template_question_repository

    def execute(self, command: CreateInterviewTemplateQuestionCommand) -> None:
        new_interview_template_question = InterviewTemplateQuestion.create(
            id=command.id,
            interview_template_section_id=command.interview_template_section_id,
            sort_order=command.sort_order,
            name=command.name,
            description=command.description,
            data_type=command.data_type,
            code=command.code,
            scope=command.scope,
            allow_ai_followup=command.allow_ai_followup,
            legal_notice=command.legal_notice
        )
        self.interview_template_question_repository.create(new_interview_template_question)
