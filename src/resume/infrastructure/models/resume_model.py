from datetime import datetime
from typing import Dict, Any, Optional

from sqlalchemy import String, DateTime, JSON, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.sql import func

from core.database import Base


class ResumeModel(Base):
    """Modelo SQLAlchemy para Resume - Matching actual database schema"""

    __tablename__ = "resumes"

    # Primary fields - matching actual database structure
    id: Mapped[str] = mapped_column(String, primary_key=True)
    candidate_id: Mapped[str] = mapped_column(String, ForeignKey("candidates.id"), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    resume_type: Mapped[str] = mapped_column(String, nullable=False, index=True)

    # Optional fields
    position_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    role: Mapped[Optional[str]] = mapped_column(String, nullable=True)

    # JSON content fields - matching database structure
    content_data: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    ai_content: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    custom_content: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    formatting_preferences: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, server_default=func.now())
    last_generated_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)

    def __repr__(self) -> str:
        return f"<ResumeModel(id='{self.id}', name='{self.name}', type='{self.resume_type}')>"
