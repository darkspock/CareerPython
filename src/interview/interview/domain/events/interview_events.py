"""Interview domain events"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.shared.domain.events.domain_event import DomainEvent


@dataclass
class InterviewCreatedEvent(DomainEvent):
    """Event raised when an interview is created"""
    interview_id: str
    candidate_id: str
    job_position_id: Optional[str]
    interview_template_id: Optional[str]
    interview_type: str
    created_at: datetime


@dataclass
class InterviewStartedEvent(DomainEvent):
    """Event raised when an interview is started"""
    interview_id: str
    candidate_id: str
    started_at: datetime
    started_by: Optional[str]


@dataclass
class InterviewFinishedEvent(DomainEvent):
    """Event raised when an interview is finished"""
    interview_id: str
    candidate_id: str
    finished_at: datetime
    duration_minutes: Optional[int]
    score: Optional[float]
    finished_by: Optional[str]


@dataclass
class InterviewPausedEvent(DomainEvent):
    """Event raised when an interview is paused"""
    interview_id: str
    candidate_id: str
    paused_at: datetime
    paused_by: Optional[str]


@dataclass
class InterviewResumedEvent(DomainEvent):
    """Event raised when an interview is resumed"""
    interview_id: str
    candidate_id: str
    resumed_at: datetime
    resumed_by: Optional[str]


@dataclass
class InterviewDiscardedEvent(DomainEvent):
    """Event raised when an interview is discarded"""
    interview_id: str
    candidate_id: str
    discarded_at: datetime
    discarded_by: Optional[str]


@dataclass
class InterviewScheduledEvent(DomainEvent):
    """Event raised when an interview is scheduled"""
    interview_id: str
    candidate_id: str
    scheduled_at: datetime
    scheduled_by: Optional[str]


@dataclass
class InterviewScoredEvent(DomainEvent):
    """Event raised when an interview is scored"""
    interview_id: str
    candidate_id: str
    score: float
    scored_at: datetime
    scored_by: Optional[str]
