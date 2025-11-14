"""Interview SQLAlchemy model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, DateTime, Integer, Float, Text, JSON, ForeignKey, func
from sqlalchemy.dialects import postgresql
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.framework.domain.entities.base import generate_id
# Removed import to avoid circular dependency
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum
)

# Forward references for mypy
if TYPE_CHECKING:
    from src.company_bc.candidate_application.infrastructure.models.candidate_application_model import \
        CandidateApplicationModel
    from src.interview_bc.interview.Infrastructure.models.interview_answer_model import InterviewAnswerModel


@dataclass
class InterviewModel(Base):
    """SQLAlchemy model for interviews"""
    __tablename__ = "interviews"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    candidate_id: Mapped[str] = mapped_column(String, index=True)
    job_position_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    application_id: Mapped[Optional[str]] = mapped_column(String, ForeignKey("candidate_applications.id"), index=True)
    interview_template_id: Mapped[Optional[str]] = mapped_column(String, index=True)
    workflow_stage_id: Mapped[Optional[str]] = mapped_column(String,
                                                             ForeignKey("workflow_stages.id", ondelete="SET NULL"),
                                                             index=True, nullable=True)
    process_type: Mapped[Optional[str]] = mapped_column(String, nullable=True,
                                                        index=True)  # Stored as VARCHAR, validated in domain layer
    interview_type: Mapped[str] = mapped_column(String,
                                                default=InterviewTypeEnum.CUSTOM.value)  # Stored as VARCHAR, validated in domain layer
    interview_mode: Mapped[Optional[str]] = mapped_column(String, nullable=True,
                                                          index=True)  # Stored as VARCHAR, validated in domain layer
    status: Mapped[str] = mapped_column(String,
                                        default=InterviewStatusEnum.ENABLED.value)  # Stored as VARCHAR, validated in domain layer
    title: Mapped[Optional[str]] = mapped_column(String)
    description: Mapped[Optional[str]] = mapped_column(Text)
    scheduled_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    deadline_date: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)  # Optional deadline date
    # List of CompanyRole IDs (obligatory in domain, nullable in DB for migration)
    required_roles: Mapped[Optional[List[str]]] = mapped_column(
        postgresql.JSONB, nullable=True
    )
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    finished_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    duration_minutes: Mapped[Optional[int]] = mapped_column(Integer)
    interviewers: Mapped[Optional[List[str]]] = mapped_column(JSON)  # List of interviewer names
    interviewer_notes: Mapped[Optional[str]] = mapped_column(Text)
    candidate_notes: Mapped[Optional[str]] = mapped_column(Text)
    score: Mapped[Optional[float]] = mapped_column(Float)  # Overall interview score (0-100)
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    free_answers: Mapped[Optional[str]] = mapped_column(Text)  # Free text answers from candidate
    link_token: Mapped[Optional[str]] = mapped_column(String, nullable=True,
                                                      index=True)  # Unique token for secure interview link access
    link_expires_at: Mapped[Optional[datetime]] = mapped_column(DateTime,
                                                                nullable=True)  # Expiration date for the interview link
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[str]] = mapped_column(String)  # User ID who created the interview
    updated_by: Mapped[Optional[str]] = mapped_column(String)  # User ID who last updated the interview

    # Relationships
    answers: Mapped[List["InterviewAnswerModel"]] = relationship(  # noqa: F821
        back_populates="interview", cascade="all, delete-orphan"
    )
    interviewer_relations: Mapped[List["InterviewInterviewerModel"]] = relationship(  # type: ignore # noqa: F821
        "InterviewInterviewerModel",
        back_populates="interview",
        cascade="all, delete-orphan"
    )
    application: Mapped[Optional["CandidateApplicationModel"]] = relationship("CandidateApplicationModel",
                                                                              back_populates="interviews")

    def __repr__(self) -> str:
        return f"<InterviewModel(id={self.id}, candidate_id={self.candidate_id}, status={self.status})>"
