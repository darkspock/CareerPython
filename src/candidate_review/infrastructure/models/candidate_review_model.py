from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Text, Integer, DateTime, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.candidate_review.domain.enums import (
    ReviewStatusEnum,
    ReviewScoreEnum,
)


@dataclass
class CandidateReviewModel(Base):
    """SQLAlchemy model for CandidateReview"""
    __tablename__ = "candidate_reviews"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_candidate_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    score: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        index=True
    )
    comment: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
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
    review_status: Mapped[str] = mapped_column(
        SQLEnum(ReviewStatusEnum, native_enum=False, length=20),
        nullable=False,
        default=ReviewStatusEnum.REVIEWED.value,
        index=True
    )
    created_by_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_users.id", ondelete="SET NULL"),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

