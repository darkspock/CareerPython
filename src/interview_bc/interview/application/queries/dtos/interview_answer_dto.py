"""Interview Answer DTO for application layer"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.interview_bc.interview.domain.entities.interview_answer import InterviewAnswer
from src.interview_bc.interview.domain.value_objects.interview_answer_id import InterviewAnswerId
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects import InterviewTemplateQuestionId


@dataclass
class InterviewAnswerDto:
    id: InterviewAnswerId
    interview_id: InterviewId
    question_id: InterviewTemplateQuestionId
    question_text: Optional[str]
    answer_text: Optional[str]
    score: Optional[float]
    feedback: Optional[str]
    answered_at: Optional[datetime]
    scored_at: Optional[datetime]
    scored_by: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]
    created_by: Optional[str]
    updated_by: Optional[str]

    @classmethod
    def from_entity(cls, entity: InterviewAnswer) -> "InterviewAnswerDto":
        """Convert domain entity to DTO"""
        return cls(
            id=entity.id,
            interview_id=entity.interview_id,
            question_id=entity.question_id,
            question_text=entity.question_text,
            answer_text=entity.answer_text,
            score=entity.score,
            feedback=entity.feedback,
            answered_at=entity.answered_at,
            scored_at=entity.scored_at,
            scored_by=entity.scored_by,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            created_by=entity.created_by,
            updated_by=entity.updated_by
        )
