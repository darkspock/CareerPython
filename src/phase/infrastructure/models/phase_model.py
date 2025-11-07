"""Phase SQLAlchemy model"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Integer, Text, DateTime, Enum, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.enums.phase_status_enum import PhaseStatus
from src.shared.domain.entities.base import generate_id
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum


@dataclass
class PhaseModel(Base):
    """SQLAlchemy model for company phases"""
    __tablename__ = "company_phases"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    company_id: Mapped[str] = mapped_column(String, index=True, nullable=False)
    workflow_type: Mapped[str] = mapped_column(String, nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    default_view: Mapped[DefaultView] = mapped_column(Enum(DefaultView, name='defaultview', create_type=False), nullable=False)
    status: Mapped[PhaseStatus] = mapped_column(Enum(PhaseStatus, name='phasestatus', create_type=False), nullable=False, default=PhaseStatus.ACTIVE, index=True)
    objective: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now(), onupdate=func.now(), nullable=False)

    def __repr__(self) -> str:
        return f"<PhaseModel(id={self.id}, name={self.name}, sort_order={self.sort_order})>"
