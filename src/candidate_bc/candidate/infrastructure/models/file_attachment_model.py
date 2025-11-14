from dataclasses import dataclass
from sqlalchemy import String, DateTime, Integer, Text, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.sql import func
from core.base import Base
from typing import TYPE_CHECKING, Optional
from datetime import datetime

if TYPE_CHECKING:
    from src.candidate_bc.candidate.infrastructure.models.candidate_model import CandidateModel


@dataclass
class FileAttachmentModel(Base):
    """SQLAlchemy model for file attachments"""
    __tablename__ = "file_attachments"

    id: Mapped[str] = mapped_column(String, primary_key=True)
    candidate_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True
    )
    filename: Mapped[str] = mapped_column(String, nullable=False)
    original_name: Mapped[str] = mapped_column(String, nullable=False)
    file_path: Mapped[str] = mapped_column(String, nullable=False)
    file_url: Mapped[str] = mapped_column(String, nullable=False)
    content_type: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    uploaded_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    # Relationship
    candidate: Mapped["CandidateModel"] = relationship("CandidateModel", back_populates="file_attachments")

    def __repr__(self) -> str:
        return f"<FileAttachmentModel(id={self.id}, candidate_id={self.candidate_id}, filename={self.filename})>"
