"""Interview Answer domain entity"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from src.interview.interview.domain.value_objects.interview_answer_id import InterviewAnswerId
from src.interview.interview.domain.value_objects.interview_id import InterviewId
from src.interview.interview_template.domain.value_objects.interview_template_question_id import \
    InterviewTemplateQuestionId


@dataclass
class InterviewAnswer:
    """Interview Answer entity"""
    id: InterviewAnswerId
    interview_id: InterviewId
    question_id: InterviewTemplateQuestionId
    question_text: Optional[str] = None
    answer_text: Optional[str] = None
    score: Optional[float] = None
    feedback: Optional[str] = None
    answered_at: Optional[datetime] = None
    scored_at: Optional[datetime] = None
    scored_by: Optional[str] = None
    created_at: Optional[datetime] = field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    created_by: Optional[str] = None
    updated_by: Optional[str] = None
