"""Interview Answer SQLAlchemy model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Float, DateTime, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from src.interview.interview.Infrastructure.models.interview_model import InterviewModel


@dataclass
class InterviewAnswerModel(Base):
    """Interview Answer database model"""
    __tablename__ = "interview_answers"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    interview_id: Mapped[str] = mapped_column(String, ForeignKey("interviews.id"), index=True)
    question_id: Mapped[str] = mapped_column(String, index=True)
    question_text: Mapped[Optional[str]] = mapped_column(Text)
    answer_text: Mapped[Optional[str]] = mapped_column(Text)
    score: Mapped[Optional[float]] = mapped_column(Float)
    feedback: Mapped[Optional[str]] = mapped_column(Text)
    answered_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scored_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    scored_by: Mapped[Optional[str]] = mapped_column(String)
    created_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime)
    created_by: Mapped[Optional[str]] = mapped_column(String)
    updated_by: Mapped[Optional[str]] = mapped_column(String)
    interview: Mapped["InterviewModel"] = relationship(back_populates="answers")
