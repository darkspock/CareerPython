from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any
from sqlalchemy import String, Integer, Boolean, Enum as SQLEnum, ForeignKey, JSON, Text, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum


@dataclass
class WorkflowStageModel(Base):
    """SQLAlchemy model for workflow stage"""
    __tablename__ = "workflow_stages"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(String, ForeignKey("workflows.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False, default="")
    stage_type: Mapped[str] = mapped_column(
        SQLEnum(WorkflowStageTypeEnum, native_enum=False, length=20),
        nullable=False,
        default=WorkflowStageTypeEnum.INITIAL.value
    )
    order: Mapped[int] = mapped_column(Integer, nullable=False, default=0, index=True)
    allow_skip: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    estimated_duration_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    # Phase 2: Enhanced configuration fields
    default_role_ids: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)  # Array of role IDs
    default_assigned_users: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)  # Array of user IDs
    email_template_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # FK to email_templates
    custom_email_text: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    deadline_days: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)  # Days to complete stage
    estimated_cost: Mapped[Optional[float]] = mapped_column(Numeric(10, 2), nullable=True)  # Cost tracking

    # Phase 12: Phase transition
    next_phase_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)  # Phase to transition to (only for SUCCESS/FAIL stages)

    # Kanban display configuration
    kanban_display: Mapped[str] = mapped_column(String(10), nullable=False, default='column')  # 'column', 'row', or 'none'

    # Visual styling
    style: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # StageStyle as JSON

    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
