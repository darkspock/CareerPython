from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from sqlalchemy import String, DateTime, ForeignKey, func, UniqueConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.company.domain.enums import CompanyUserInvitationStatus


@dataclass
class CompanyUserInvitationModel(Base):
    """SQLAlchemy model for company user invitations"""
    __tablename__ = "company_user_invitations"
    __table_args__ = (
        UniqueConstraint('token', name='uq_invitation_token'),
        Index('ix_invitation_email_company', 'email', 'company_id'),
        Index('ix_invitation_token', 'token'),
        Index('ix_invitation_email', 'email'),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    email: Mapped[str] = mapped_column(String, nullable=False, index=True)
    invited_by_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_users.id", ondelete="SET NULL"),
        nullable=False
    )
    token: Mapped[str] = mapped_column(String, unique=True, nullable=False, index=True)
    status: Mapped[str] = mapped_column(
        String,
        nullable=False,
        default=CompanyUserInvitationStatus.PENDING.value
    )
    expires_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    accepted_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    rejected_at: Mapped[Optional[datetime]] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<CompanyUserInvitationModel(id={self.id}, email={self.email}, status={self.status})>"

