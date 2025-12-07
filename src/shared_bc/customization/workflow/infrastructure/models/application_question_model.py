from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from sqlalchemy import String, Boolean, Integer, Enum as SQLEnum, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.shared_bc.customization.workflow.domain.enums.application_question_field_type import (
    ApplicationQuestionFieldType
)


@dataclass
class ApplicationQuestionModel(Base):
    """SQLAlchemy model for application questions."""
    __tablename__ = "application_questions"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    workflow_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("workflows.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    company_id: Mapped[str] = mapped_column(String, nullable=False, index=True)
    field_key: Mapped[str] = mapped_column(String(100), nullable=False)
    label: Mapped[str] = mapped_column(String(500), nullable=False)
    description: Mapped[Optional[str]] = mapped_column(String(1000), nullable=True)
    field_type: Mapped[str] = mapped_column(
        SQLEnum(ApplicationQuestionFieldType, native_enum=False, length=20),
        nullable=False
    )
    options: Mapped[Optional[List[str]]] = mapped_column(JSON, nullable=True)
    is_required_default: Mapped[bool] = mapped_column(Boolean, nullable=False, default=False)
    validation_rules: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    sort_order: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True, index=True)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    __table_args__ = (
        # Unique constraint on workflow_id + field_key
        {'sqlite_autoincrement': True},
    )
