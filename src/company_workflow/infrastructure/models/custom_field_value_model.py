from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import String, ForeignKey, JSON, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


@dataclass
class CustomFieldValueModel(Base):
    """
    SQLAlchemy model for custom field values
    Stores all custom field values for a candidate+workflow in a single JSON for better performance
    """
    __tablename__ = "custom_field_values"

    id: Mapped[str] = mapped_column(String(255), primary_key=True)
    company_candidate_id: Mapped[str] = mapped_column(String(255),
                                                      ForeignKey("company_candidates.id", ondelete="CASCADE"),
                                                      nullable=False, index=True)
    workflow_id: Mapped[str] = mapped_column(String(255), ForeignKey("company_workflows.id", ondelete="CASCADE"),
                                             nullable=False, index=True)
    # JSON with all field values, keyed by field_id (not field_key, to avoid data loss on rename)
    values: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow,
                                                 onupdate=datetime.utcnow)

    # Composite unique constraint on company_candidate_id + workflow_id
    __table_args__ = (
        {'extend_existing': True}
    )
