"""Public interview schemas for token-based access"""
from typing import Optional, List, Dict
from pydantic import BaseModel, Field


class InterviewQuestionPublicResponse(BaseModel):
    """Public question response schema"""
    id: str
    name: str
    description: Optional[str] = None
    code: Optional[str] = None
    sort_order: int
    interview_template_section_id: str
    scope: Optional[str] = None
    data_type: Optional[str] = None
    status: Optional[str] = None
    allow_ai_followup: Optional[bool] = None
    legal_notice: Optional[str] = None


class InterviewSectionPublicResponse(BaseModel):
    """Public section response schema"""
    id: str
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    sort_order: int
    section: Optional[str] = None
    status: Optional[str] = None
    questions: List[InterviewQuestionPublicResponse] = Field(default_factory=list)


class InterviewTemplatePublicResponse(BaseModel):
    """Public template response schema"""
    id: str
    name: str
    intro: Optional[str] = None
    prompt: Optional[str] = None
    goal: Optional[str] = None
    scoring_mode: Optional[str] = None
    sections: List[InterviewSectionPublicResponse] = Field(default_factory=list)


class InterviewQuestionsPublicResponse(BaseModel):
    """Public interview questions response"""
    interview_id: str
    interview_title: Optional[str] = None
    interview_description: Optional[str] = None
    template: Optional[InterviewTemplatePublicResponse] = None
    existing_answers: Dict[str, Optional[str]] = Field(default_factory=dict)


class SubmitAnswerRequest(BaseModel):
    """Request to submit an answer"""
    question_id: str = Field(..., description="Question ID")
    answer_text: Optional[str] = Field(None, description="Answer text")
    question_text: Optional[str] = Field(None, description="Question text (for reference)")


class SubmitAnswerResponse(BaseModel):
    """Response after submitting an answer"""
    message: str
    status: str

