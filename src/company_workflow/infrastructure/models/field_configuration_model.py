from dataclasses import dataclass
from datetime import datetime
from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class FieldConfigurationModel(Base):
    """SQLAlchemy model for field configuration"""
    __tablename__ = "stage_field_configurations"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    stage_id: Mapped[str] = mapped_column(String(255), ForeignKey("workflow_stages.id", ondelete="CASCADE"), nullable=False, index=True)
    custom_field_id: Mapped[str] = mapped_column(String(255), ForeignKey("workflow_custom_fields.id", ondelete="CASCADE"), nullable=False, index=True)
    visibility: Mapped[str] = mapped_column(String(50), nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)
