from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import String, ForeignKey, Index, UniqueConstraint
from sqlalchemy.dialects.postgresql import JSON
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class CustomFieldValueModel(Base):
    """SQLAlchemy model for custom field values"""
    __tablename__ = "custom_field_values"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    entity_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    # For backward compatibility during migration - can be removed later
    company_candidate_id: Mapped[str] = mapped_column(
        String(255),
        ForeignKey("company_candidates.id", ondelete="CASCADE"),
        nullable=True,
        index=True
    )
    values: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)  # {field_key: value}
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint: one value set per entity
    __table_args__ = (
        UniqueConstraint('entity_type', 'entity_id', name='uq_custom_field_values_entity_type_id'),
        Index('ix_custom_field_values_entity_type_id', 'entity_type', 'entity_id'),
        Index('ix_custom_field_values_company_candidate_id', 'company_candidate_id'),
    )
