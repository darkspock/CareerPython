"""JobPositionStage SQLAlchemy model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

from sqlalchemy import String, DateTime, Text, JSON, Numeric, func, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.framework.domain.entities.base import generate_id


@dataclass
class JobPositionStageModel(Base):
    """SQLAlchemy model for job position stage tracking"""
    __tablename__ = "job_position_stages"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    job_position_id: Mapped[str] = mapped_column(
        String(26),
        ForeignKey('job_positions.id', ondelete='CASCADE'),
        nullable=False,
        index=True
    )
    phase_id: Mapped[Optional[str]] = mapped_column(
        String,
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
        return f"<JobPositionStageModel(id={self.id}, job_position_id={self.job_position_id}, stage_id={self.stage_id})>"

