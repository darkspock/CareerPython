from dataclasses import dataclass
from datetime import datetime
from typing import Any, Optional
from sqlalchemy import String, Boolean, DateTime, Text, JSON
from sqlalchemy.orm import Mapped, mapped_column
from core.database import Base


@dataclass
class ValidationRuleModel(Base):
    """SQLAlchemy model for validation rules."""

    __tablename__ = "field_validation_rules"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    custom_field_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    stage_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    rule_type: Mapped[str] = mapped_column(String(50), nullable=False)
    comparison_operator: Mapped[str] = mapped_column(String(50), nullable=False)
    position_field_path: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    comparison_value: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
    validation_message: Mapped[str] = mapped_column(Text, nullable=False)
    auto_reject: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='false')
    rejection_reason: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, server_default='true', index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
