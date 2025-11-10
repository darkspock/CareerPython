from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from sqlalchemy import String, Date, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.framework.domain.entities.base import generate_id


@dataclass
class CandidateProjectModel(Base):
    """Modelo de SQLAlchemy para proyectos de candidatos"""
    __tablename__ = "candidate_projects"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey('candidates.id'))
    name: Mapped[str] = mapped_column(String)
    description: Mapped[str] = mapped_column(String)
    start_date: Mapped[date] = mapped_column(Date)
    end_date: Mapped[Optional[date]] = mapped_column(Date)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)

    candidate: Mapped["CandidateModel"] = relationship(back_populates="projects")   # type: ignore # noqa: F821
