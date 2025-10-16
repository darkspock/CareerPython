"""Interview Answer domain events"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.shared.domain.events.domain_event import DomainEvent


@dataclass
class InterviewAnswerCreatedEvent(DomainEvent):
    """Event published when an interview answer is created"""
    answer_id: str
    interview_id: str
    question_id: str
    answer_text: Optional[str]
    answered_at: datetime
    created_by: Optional[str] = None


@dataclass
class InterviewAnswerUpdatedEvent(DomainEvent):
    """Event published when an interview answer is updated"""
    answer_id: str
    interview_id: str
    question_id: str
    answer_text: Optional[str]
    updated_at: datetime
    updated_by: Optional[str] = None


@dataclass
class InterviewAnswerScoredEvent(DomainEvent):
    """Event published when an interview answer is scored"""
    answer_id: str
    interview_id: str
    question_id: str
    score: Optional[float]
    feedback: Optional[str]
    scored_at: datetime
    scored_by: Optional[str]


@dataclass
class InterviewAnswerDeletedEvent(DomainEvent):
    """Event published when an interview answer is deleted"""
    answer_id: str
    interview_id: str
    question_id: str
    deleted_at: datetime
    deleted_by: Optional[str] = None
