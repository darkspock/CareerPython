"""CandidateStage SQLAlchemy model"""
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Dict, Any

from sqlalchemy import String, DateTime, Text, JSON, Numeric, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.framework.domain.entities.base import generate_id


@dataclass
class CandidateApplicationStageModel(Base):
    """SQLAlchemy model for candidate stage tracking"""
    __tablename__ = "candidate_application_stages"

    id: Mapped[str] = mapped_column(String(26), primary_key=True, index=True, default=generate_id)
    candidate_application_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('candidate_applications.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    phase_id: Mapped[Optional[str]] = mapped_column(
        String(26),
        ForeignKey('company_phases.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    workflow_id: Mapped[Optional[str]] = mapped_column(
        String(26),
        ForeignKey('workflows.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    stage_id: Mapped[Optional[str]] = mapped_column(
        String(26),
        ForeignKey('workflow_stages.id', ondelete='SET NULL'),
        nullable=True,
        index=True
    )
    started_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    deadline: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    estimated_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    actual_cost: Mapped[Optional[Decimal]] = mapped_column(Numeric(10, 2), nullable=True)
    comments: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<CandidateStageModel(id={self.id}, candidate_application_id={self.candidate_application_id}, phase_id={self.phase_id})>"
