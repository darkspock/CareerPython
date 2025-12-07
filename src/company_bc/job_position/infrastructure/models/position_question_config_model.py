from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, Boolean, Integer, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class PositionQuestionConfigModel(Base):
    """SQLAlchemy model for position question configurations."""
    __tablename__ = "position_question_configs"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    position_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("job_positions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    question_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("application_questions.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    enabled: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    is_required_override: Mapped[Optional[bool]] = mapped_column(Boolean, nullable=True)
    sort_order_override: Mapped[Optional[int]] = mapped_column(Integer, nullable=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        UniqueConstraint('position_id', 'question_id', name='uq_position_question'),
    )
