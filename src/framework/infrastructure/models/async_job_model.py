"""SQLAlchemy model for AsyncJob."""

from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, Integer, DateTime, Text, JSON, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.framework.domain.entities.base import generate_id


@dataclass
class AsyncJobModel(Base):
    """SQLAlchemy model for async jobs."""
    __tablename__ = "async_jobs"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True, default=generate_id)
    job_type: Mapped[str] = mapped_column(String(50), nullable=False, index=True)
    entity_type: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    entity_id: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    status: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    progress: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    started_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    results: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    error_message: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    job_metadata: Mapped[Optional[Dict[str, Any]]] = mapped_column(JSON, nullable=True)
    timeout_seconds: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())
