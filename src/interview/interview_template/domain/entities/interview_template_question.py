from dataclasses import dataclass
from typing import Optional

from src.interview.interview_template.domain.enums.interview_template_question import \
    InterviewTemplateQuestionStatusEnum, \
    InterviewTemplateQuestionDataTypeEnum, InterviewTemplateQuestionScopeEnum
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId
from src.interview.interview_template.domain.value_objects.interview_template_section_id import \
    InterviewTemplateSectionId


@dataclass
class InterviewTemplateQuestion:
    id: InterviewTemplateQuestionId
    interview_template_section_id: InterviewTemplateSectionId
    sort_order: int
    name: str
    description: str
    data_type: InterviewTemplateQuestionDataTypeEnum
    scope: InterviewTemplateQuestionScopeEnum
    code: str
    status: InterviewTemplateQuestionStatusEnum = InterviewTemplateQuestionStatusEnum.DRAFT
    allow_ai_followup: bool = False  # If True, AI can generate follow-up questions based on this question
    legal_notice: Optional[str] = None  # Legal text displayed to users for compliance

    @staticmethod
    def create(id: InterviewTemplateQuestionId, interview_template_section_id: InterviewTemplateSectionId,
               sort_order: int, name: str, description: str,
               data_type: InterviewTemplateQuestionDataTypeEnum, scope: InterviewTemplateQuestionScopeEnum,
               code: str,
               status: InterviewTemplateQuestionStatusEnum = InterviewTemplateQuestionStatusEnum.DRAFT,
               allow_ai_followup: bool = False,
               legal_notice: Optional[str] = None) -> 'InterviewTemplateQuestion':
        return InterviewTemplateQuestion(
            id=id,
            interview_template_section_id=interview_template_section_id,
            sort_order=sort_order,
            name=name,
            description=description,
            status=status,
            data_type=data_type,
            scope=scope,
            code=code,
            allow_ai_followup=allow_ai_followup,
            legal_notice=legal_notice
        )

    def update_details(self, interview_template_section_id: InterviewTemplateSectionId,
                       sort_order: int,
                       name: str,
                       description: str,
                       data_type: InterviewTemplateQuestionDataTypeEnum,
                       scope: InterviewTemplateQuestionScopeEnum,
                       code: str,
                       allow_ai_followup: bool = False,
                       legal_notice: Optional[str] = None) -> None:
        self.sort_order = sort_order
        self.name = name
        self.description = description
        self.data_type = data_type
        self.scope = scope
        self.code = code
        self.interview_template_section_id = interview_template_section_id
        self.allow_ai_followup = allow_ai_followup
        self.legal_notice = legal_notice

    def enable(self) -> None:
        """Enable this interview template question"""
        self.status = InterviewTemplateQuestionStatusEnum.ENABLED

    def disable(self) -> None:
        """Disable this interview template question"""
        self.status = InterviewTemplateQuestionStatusEnum.DISABLED

    def publish(self) -> None:
        """Publish this interview template question"""
        self.status = InterviewTemplateQuestionStatusEnum.ENABLED

    def draft(self) -> None:
        """Set this interview template question to draft status"""
        self.status = InterviewTemplateQuestionStatusEnum.DRAFT
