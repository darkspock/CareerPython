from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Enum, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.shared.domain.entities.base import generate_id

# Forward references for mypy
if TYPE_CHECKING:
    from src.candidate.infrastructure.models.candidate_model import CandidateModel
    from src.job_position.infrastructure.models.job_position_model import JobPositionModel
    from src.interview.interview.Infrastructure.models.interview_model import InterviewModel


@dataclass
class CandidateApplicationModel(Base):
    """Modelo de SQLAlchemy para aplicaciones de candidatos"""
    __tablename__ = "candidate_applications"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey("candidates.id"), nullable=False, index=True)
    job_position_id: Mapped[str] = mapped_column(String, ForeignKey("job_positions.id"), nullable=False, index=True)
    application_status: Mapped[ApplicationStatusEnum] = mapped_column(
        Enum(ApplicationStatusEnum, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=ApplicationStatusEnum.APPLIED,
        index=True
    )
    applied_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True, onupdate=func.now())
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)

    # Relationships
    candidate: Mapped["CandidateModel"] = relationship("CandidateModel", back_populates="applications")
    job_position: Mapped["JobPositionModel"] = relationship("JobPositionModel", back_populates="applications")
    interviews: Mapped[List["InterviewModel"]] = relationship("InterviewModel", back_populates="application")
