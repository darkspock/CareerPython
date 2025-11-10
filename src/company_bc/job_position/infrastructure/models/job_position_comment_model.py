"""Job Position Comment SQLAlchemy Model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.company_bc.job_position.domain.enums import (
    CommentVisibilityEnum,
    CommentReviewStatusEnum,
)


@dataclass
class JobPositionCommentModel(Base):
    """SQLAlchemy model for JobPositionComment"""
    __tablename__ = "job_position_comments"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    job_position_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("job_positions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    workflow_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("job_position_workflows.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    stage_id: Mapped[Optional[str]] = mapped_column(
        String,
        nullable=True,
        index=True
    )
    job_position_stage_id: Mapped[Optional[str]] = mapped_column(
        String(26),
        ForeignKey("job_position_stages.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    created_by_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_users.id", ondelete="SET NULL"),
        nullable=False,
        index=True
    )
    review_status: Mapped[str] = mapped_column(
        SQLEnum(CommentReviewStatusEnum, native_enum=False, length=20),
        nullable=False,
        default=CommentReviewStatusEnum.REVIEWED.value,
        index=True
    )
    visibility: Mapped[str] = mapped_column(
        SQLEnum(CommentVisibilityEnum, native_enum=False, length=30),
        nullable=False,
        default=CommentVisibilityEnum.SHARED.value
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

