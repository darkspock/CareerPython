from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.company_bc.company_candidate.domain.enums import (
    CommentVisibility,
    CommentReviewStatus,
)


@dataclass
class CandidateCommentModel(Base):
    """SQLAlchemy model for CandidateComment"""
    __tablename__ = "candidate_comments"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_candidate_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    comment: Mapped[str] = mapped_column(Text, nullable=False)
    workflow_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("workflows.id", ondelete="SET NULL"),
        nullable=True,
        index=True
    )
    stage_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("workflow_stages.id", ondelete="SET NULL"),
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
        SQLEnum(CommentReviewStatus, native_enum=False, length=20),
        nullable=False,
        default=CommentReviewStatus.REVIEWED.value,
        index=True
    )
    visibility: Mapped[str] = mapped_column(
        SQLEnum(CommentVisibility, native_enum=False, length=30),
        nullable=False,
        default=CommentVisibility.PRIVATE.value
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

