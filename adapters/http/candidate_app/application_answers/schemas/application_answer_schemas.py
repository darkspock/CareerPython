"""Schemas for Application Question Answers endpoints"""
from typing import Optional, List, Any
from datetime import datetime
from pydantic import BaseModel, Field


class AnswerInput(BaseModel):
    """Input for a single question answer."""
    question_id: str = Field(..., description="The application question ID")
    answer_value: Any = Field(..., description="The answer value (type depends on question type)")


class SaveAnswersRequest(BaseModel):
    """Request to save question answers for an application."""
    answers: List[AnswerInput] = Field(..., description="List of answers to save")


class ApplicationAnswerResponse(BaseModel):
    """Response for a single application answer."""
    id: str
    application_id: str
    question_id: str
    answer_value: Any
    created_at: datetime
    updated_at: datetime


class ApplicationAnswerListResponse(BaseModel):
    """Response for list of application answers."""
    answers: List[ApplicationAnswerResponse]
    total: int


class EnabledQuestionResponse(BaseModel):
    """Response for an enabled question (for public form display)."""
    id: str
    workflow_id: str
    field_key: str
    label: str
    field_type: str
    description: Optional[str]
    options: Optional[List[Any]]
    is_required: bool
    sort_order: int
    validation_rules: Optional[dict]


class EnabledQuestionsListResponse(BaseModel):
    """Response for list of enabled questions for a position."""
    questions: List[EnabledQuestionResponse]
    total: int
    position_id: str
    workflow_id: Optional[str]
