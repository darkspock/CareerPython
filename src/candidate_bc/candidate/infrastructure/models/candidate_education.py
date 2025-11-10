from datetime import datetime, date
from typing import Optional

from sqlalchemy import ForeignKey, String, Date, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.database import Base
from src.framework.domain.entities.base import generate_id


class CandidateEducationModel(Base):
    """Modelo de SQLAlchemy para educación de candidatos"""
    __tablename__ = "candidate_educations"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey('candidates.id'))
    degree: Mapped[str] = mapped_column(String)
    institution: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    candidate: Mapped["CandidateModel"] = relationship(back_populates="educations")  # type: ignore # noqa: F821
