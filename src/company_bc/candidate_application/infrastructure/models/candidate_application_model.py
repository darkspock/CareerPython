from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List, TYPE_CHECKING

from sqlalchemy import String, Enum, DateTime, Text, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.base import Base
from src.company_bc.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.company_bc.candidate_application.domain.enums.task_status import TaskStatus
from src.framework.domain.entities.base import generate_id

# Forward references for mypy
if TYPE_CHECKING:
    from src.candidate_bc.candidate.infrastructure import CandidateModel
    from src.company_bc.job_position.infrastructure.models.job_position_model import JobPositionModel
    from src.interview_bc.interview.Infrastructure.models.interview_model import InterviewModel


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

    # Workflow stage tracking fields (Phase 5)
    current_stage_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("workflow_stages.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    stage_entered_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    stage_deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    task_status: Mapped[TaskStatus] = mapped_column(
        Enum(TaskStatus, values_callable=lambda x: [e.value for e in x]),
        nullable=False,
        default=TaskStatus.PENDING
    )

    # Phase 12: Phase tracking field
    current_phase_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("company_phases.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )

    # Relationships
    candidate: Mapped["CandidateModel"] = relationship("CandidateModel", back_populates="applications")
    job_position: Mapped["JobPositionModel"] = relationship("JobPositionModel", back_populates="applications")
    interviews: Mapped[List["InterviewModel"]] = relationship("InterviewModel", back_populates="application")
