from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Any

from sqlalchemy import String, Integer, ForeignKey, JSON
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class CustomFieldModel(Base):
    """SQLAlchemy model for custom field"""
    __tablename__ = "workflow_custom_fields"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    workflow_id: Mapped[str] = mapped_column(String(255), ForeignKey("company_workflows.id", ondelete="CASCADE"),
                                             nullable=False, index=True)
    field_key: Mapped[str] = mapped_column(String(100), nullable=False)
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_type: Mapped[str] = mapped_column(String(50), nullable=False)
    field_config: Mapped[Optional[Any]] = mapped_column(JSON, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
