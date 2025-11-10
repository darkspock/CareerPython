from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from sqlalchemy import String, Text, Index, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import JSON

from core.database import Base
from src.shared_bc.customization.entity_customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum


@dataclass
class EntityCustomizationModel(Base):
    """SQLAlchemy model for entity customization"""
    __tablename__ = "entity_customizations"

    id: Mapped[str] = mapped_column(String(255), primary_key=True, index=True)
    entity_type: Mapped[str] = mapped_column(
        String(50),
        nullable=False,
        index=True
    )
    entity_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    validation: Mapped[Optional[str]] = mapped_column(Text, nullable=True)  # JSON-Logic
    metadata_json: Mapped[Optional[Dict[str, Any]]] = mapped_column('metadata', JSON, nullable=True, default=dict)
    created_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(nullable=False, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Unique constraint: one customization per entity
    __table_args__ = (
        UniqueConstraint('entity_type', 'entity_id', name='uq_entity_customizations_entity_type_id'),
        Index('ix_entity_customizations_entity_type_id', 'entity_type', 'entity_id'),
    )

