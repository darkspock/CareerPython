from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, Integer, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class CustomFieldModel(Base):
    """SQLAlchemy model for custom field"""
    __tablename__ = "custom_fields"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    entity_customization_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("entity_customizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    field_key: Mapped[str] = mapped_column(String(100), nullable=False)
    field_name: Mapped[str] = mapped_column(String(255), nullable=False)
    field_type: Mapped[str] = mapped_column(String(50), nullable=False)
    field_config: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    order_index: Mapped[int] = mapped_column(Integer, nullable=False)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint: one field_key per entity_customization
    __table_args__ = (
        UniqueConstraint('entity_customization_id', 'field_key',
                         name='uq_custom_fields_entity_customization_field_key'),
        Index('ix_custom_fields_entity_customization_id', 'entity_customization_id'),
    )
