from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from sqlalchemy import String, Boolean, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.workflow.domain.enums.workflow_status_enum import WorkflowStatusEnum
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum


@dataclass
class WorkflowModel(Base):
    """SQLAlchemy model for workflow"""
    __tablename__ = "workflows"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    workflow_type: Mapped[str] = mapped_column(
        SQLEnum(WorkflowTypeEnum, native_enum=False, length=30),
        nullable=False,
        index=True
    )
    display: Mapped[str] = mapped_column(
        SQLEnum(WorkflowDisplayEnum, native_enum=False, length=20),
        nullable=False,
        default=WorkflowDisplayEnum.KANBAN.value
    )
    phase_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)  # Phase 12: Phase association
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    status: Mapped[str] = mapped_column(
        SQLEnum(WorkflowStatusEnum, native_enum=False, length=20),
        nullable=False,
        default=WorkflowStatusEnum.DRAFT.value,
        index=True
    )
    is_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
