from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any

from sqlalchemy import String, JSON, Enum, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base
from src.company.domain.enums import CompanyStatus


@dataclass
class CompanyModel(Base):
    """SQLAlchemy model for recruiting companies"""
    __tablename__ = "companies"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    domain: Mapped[str] = mapped_column(String, nullable=False, unique=True, index=True)
    logo_url: Mapped[Optional[str]] = mapped_column(String, nullable=True)
    settings: Mapped[Dict[str, Any]] = mapped_column(JSON, nullable=False, default=dict)
    status: Mapped[str] = mapped_column(
        Enum(CompanyStatus, native_enum=False, length=20),
        nullable=False,
        default=CompanyStatus.ACTIVE.value
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now())
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False, default=func.now(), onupdate=func.now())

    def __repr__(self) -> str:
        return f"<CompanyModel(id={self.id}, name={self.name}, domain={self.domain}, status={self.status})>"
