"""
Talent Pool Entry Model
Phase 8: SQLAlchemy model for talent pool entries
"""

from sqlalchemy import Column, String, Text, Integer, DateTime, ForeignKey, Index, JSON
from sqlalchemy.sql import func

from core.database import Base


class TalentPoolEntryModel(Base):
    """SQLAlchemy model for company_talent_pool table"""

    __tablename__ = "company_talent_pool"

    id = Column(String(36), primary_key=True, nullable=False)
    company_id = Column(
        String(36),
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    candidate_id = Column(
        String(36),
        ForeignKey("candidates.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    source_application_id = Column(String(36), nullable=True)
    source_position_id = Column(String(36), nullable=True)
    added_reason = Column(Text, nullable=True)
    tags = Column(JSON, nullable=True)  # List of tags as JSON array
    rating = Column(Integer, nullable=True, index=True)
    notes = Column(Text, nullable=True)
    status = Column(String(20), nullable=False, index=True)
    added_by_user_id = Column(String(36), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    __table_args__ = (
        Index("ix_company_talent_pool_company_id", "company_id"),
        Index("ix_company_talent_pool_candidate_id", "candidate_id"),
        Index("ix_company_talent_pool_status", "status"),
        Index("ix_company_talent_pool_rating", "rating"),
    )
