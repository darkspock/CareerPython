from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from sqlalchemy import String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class FieldConfigurationModel(Base):
    """SQLAlchemy model for field configuration (visibility rules)"""
    __tablename__ = "field_configurations"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    entity_customization_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("entity_customizations.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    custom_field_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("custom_fields.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    # Context for where this configuration applies (e.g., "stage", "view", etc.)
    context_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True, index=True)
    context_id: Mapped[Optional[str]] = mapped_column(String(255), nullable=True, index=True)
    visibility: Mapped[str] = mapped_column(String(50), nullable=False)  # 'HIDDEN', 'VISIBLE', 'REQUIRED', 'READ_ONLY'
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint: one configuration per field per context
    __table_args__ = (
        UniqueConstraint(
            'entity_customization_id',
            'custom_field_id',
            'context_type',
            'context_id',
            name='uq_field_configurations_entity_field_context'
        ),
        Index('ix_field_configurations_entity_customization_id', 'entity_customization_id'),
        Index('ix_field_configurations_custom_field_id', 'custom_field_id'),
        Index('ix_field_configurations_context', 'context_type', 'context_id'),
    )

