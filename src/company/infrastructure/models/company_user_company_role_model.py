"""Company User - Company Role Association Model."""
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import String, DateTime, ForeignKey, func, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base


@dataclass
class CompanyUserCompanyRoleModel(Base):
    """SQLAlchemy model for company user - company role association (many-to-many)."""
    __tablename__ = "company_user_company_roles"
    __table_args__ = (
        UniqueConstraint('company_user_id', 'company_role_id', name='uq_company_user_role'),
    )

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    company_user_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    company_role_id: Mapped[str] = mapped_column(
        String,
        ForeignKey("company_roles.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())

    def __repr__(self) -> str:
        return f"<CompanyUserCompanyRoleModel(id={self.id}, company_user_id={self.company_user_id}, company_role_id={self.company_role_id})>"


