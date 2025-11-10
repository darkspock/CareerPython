"""Job Position Activity SQLAlchemy Model."""
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import String, Text, DateTime, ForeignKey, Enum as SQLEnum, JSON
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.company_bc.job_position.domain.enums.activity_type_enum import ActivityTypeEnum


@dataclass
class JobPositionActivityModel(Base):
    """SQLAlchemy model for JobPositionActivity"""
    __tablename__ = "job_position_activities"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    job_position_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("job_positions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    activity_type: Mapped[str] = mapped_column(
        SQLEnum(ActivityTypeEnum, native_enum=False, length=20),
        nullable=False,
        index=True
    )
    description: Mapped[str] = mapped_column(Text, nullable=False)
    performed_by_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_users.id", ondelete="SET NULL"),
        nullable=False,
        index=True
    )
    activity_metadata: Mapped[dict] = mapped_column('metadata', JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow, index=True)

