from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any

from sqlalchemy import String, JSON, Enum, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.company.domain.enums import CompanyUserRole, CompanyUserStatus


@dataclass
class CompanyUserModel(Base):
    """SQLAlchemy model for company users (recruiters, HR, managers)"""
    __tablename__ = "company_users"
    __table_args__ = (
        UniqueConstraint('company_id', 'user_id', name='uq_company_user'),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("companies.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    role: Mapped[str] = mapped_column(
        Enum(CompanyUserRole, native_enum=False, length=20),
        nullable=False
    )
    permissions: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(
        Enum(CompanyUserStatus, native_enum=False, length=20),
        nullable=False,
        default=CompanyUserStatus.ACTIVE.value
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<CompanyUserModel(id={self.id}, company_id={self.company_id}, user_id={self.user_id}, role={self.role})>"
