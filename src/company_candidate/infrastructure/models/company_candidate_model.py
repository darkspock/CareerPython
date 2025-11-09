from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any, List

from sqlalchemy import String, Text, DateTime, ForeignKey, JSON, Enum as SQLEnum, ARRAY
from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base
from src.company_candidate.domain.enums import (
    CompanyCandidateStatus,
    OwnershipStatus,
    CandidatePriority,
)


@dataclass
class CompanyCandidateModel(Base):
    """SQLAlchemy model for CompanyCandidate"""
    __tablename__ = "company_candidates"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("companies.id"),
        nullable=False,
        index=True
    )
    candidate_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("candidates.id"),
        nullable=False,
        index=True
    )
    status: Mapped[str] = mapped_column(
        SQLEnum(CompanyCandidateStatus, native_enum=False, length=30),
        nullable=False,
        default=CompanyCandidateStatus.PENDING_CONFIRMATION.value,
        index=True
    )
    ownership_status: Mapped[str] = mapped_column(
        SQLEnum(OwnershipStatus, native_enum=False, length=20),
        nullable=False,
        default=OwnershipStatus.COMPANY_OWNED.value,
        index=True
    )
    created_by_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_users.id"),
        nullable=False,
        index=True
    )
    workflow_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    current_stage_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    phase_id: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("company_phases.id"),
        nullable=True,
        index=True
    )
    invited_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    confirmed_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    archived_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    visibility_settings: Mapped[Dict[str, Any]] = mapped_column(
        JSON,
        nullable=False,
        default=dict
    )
    tags: Mapped[List[str]] = mapped_column(
        ARRAY(String),
        nullable=False,
        default=list
    )
    position: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    department: Mapped[Optional[str]] = mapped_column(String(255), nullable=True)
    priority: Mapped[str] = mapped_column(
        SQLEnum(CandidatePriority, native_enum=False, length=10),
        nullable=False,
        default=CandidatePriority.MEDIUM.value
    )
    # Resume fields
    lead_id: Mapped[Optional[str]] = mapped_column(String, nullable=True, index=True)
    source: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    resume_url: Mapped[Optional[str]] = mapped_column(String(500), nullable=True)
    resume_uploaded_by: Mapped[Optional[str]] = mapped_column(
        String,
        ForeignKey("company_users.id"),
        nullable=True
    )
    resume_uploaded_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<CompanyCandidateModel(id={self.id}, company_id={self.company_id}, candidate_id={self.candidate_id})>"
