"""Interview Interviewer SQLAlchemy model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, DateTime, Boolean, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base

# Forward references for mypy
if TYPE_CHECKING:
    from src.interview_bc.interview.Infrastructure.models.interview_model import InterviewModel


@dataclass
class InterviewInterviewerModel(Base):
    """SQLAlchemy model for interview-interviewer relationships"""
    __tablename__ = "interview_interviewers"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    interview_id: Mapped[str] = mapped_column(String, ForeignKey("interviews.id", ondelete="CASCADE"), index=True,
                                              nullable=False)
    user_id: Mapped[str] = mapped_column(String, ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    name: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    is_external: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    invited_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
    created_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    updated_by: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # Relationships
    interview: Mapped["InterviewModel"] = relationship(  # noqa: F821
        "InterviewModel", back_populates="interviewer_relations"
    )

    def __repr__(self) -> str:
        return f"<InterviewInterviewerModel(id={self.id}, interview_id={self.interview_id}, user_id={self.user_id})>"
