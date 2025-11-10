from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Date, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
# Removed import to avoid circular dependency

from core.base import Base
from src.framework.domain.entities.base import generate_id


@dataclass
class CandidateExperienceModel(Base):
    """Modelo de SQLAlchemy para experiencia laboral de candidatos"""
    __tablename__ = "candidate_experiences"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey('candidates.id'))
    job_title: Mapped[str] = mapped_column(String)
    company: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    candidate: Mapped["CandidateModel"] = relationship(back_populates="experiences")   # type: ignore # noqa: F821
