from pydantic import BaseModel
from src.interview_bc.interview_template.domain.enums.interview_template_question import (
    InterviewTemplateQuestionStatusEnum,
    InterviewTemplateQuestionDataTypeEnum,
    InterviewTemplateQuestionScopeEnum
)


class InterviewTemplateQuestionBase(BaseModel):
    interview_template_section_id: str
    sort_order: int
    name: str
    description: str
    status: InterviewTemplateQuestionStatusEnum
    data_type: InterviewTemplateQuestionDataTypeEnum
    scope: InterviewTemplateQuestionScopeEnum
    code: str

    class Config:
        use_enum_values = True


class InterviewTemplateQuestionCreate(InterviewTemplateQuestionBase):
    id: str


class InterviewTemplateQuestion(InterviewTemplateQuestionBase):
    id: str

    class Config:
        from_attributes = True


class InterviewTemplateQuestionResponse(InterviewTemplateQuestionBase):
    id: str

    class Config:
        from_attributes = True
