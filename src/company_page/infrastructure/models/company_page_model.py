"""
Company Page Model - Modelo SQLAlchemy para páginas de empresa
"""
from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import String, Text, Integer, Boolean, DateTime, JSON, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column

from core.base import Base


@dataclass
class CompanyPageModel(Base):
    """Modelo SQLAlchemy para páginas de empresa"""

    __tablename__ = "company_pages"

    # Primary Key
    id: Mapped[str] = mapped_column(String(255), primary_key=True)

    # Foreign Keys
    company_id: Mapped[str] = mapped_column(String(255), ForeignKey("companies.id"), nullable=False)

    # Basic Fields
    page_type: Mapped[str] = mapped_column(String(50), nullable=False)  # Enum PageType
    title: Mapped[str] = mapped_column(String(500), nullable=False)

    # Content Fields
    html_content: Mapped[str] = mapped_column(Text, nullable=False)
    plain_text: Mapped[str] = mapped_column(Text, nullable=False)
    word_count: Mapped[int] = mapped_column(Integer, nullable=False)

    # SEO Fields
    meta_description: Mapped[str | None] = mapped_column(Text)
    meta_keywords: Mapped[list[str] | None] = mapped_column(JSON)  # Array de strings
    language: Mapped[str] = mapped_column(String(10), default="es")

    # Status Fields
    status: Mapped[str] = mapped_column(String(50), nullable=False)  # Enum PageStatus
    is_default: Mapped[bool] = mapped_column(Boolean, default=False)
    version: Mapped[int] = mapped_column(Integer, default=1)

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    published_at: Mapped[datetime | None] = mapped_column(DateTime)

    # Relationships - None currently used

    # Indexes for performance
    __table_args__ = (
        Index("idx_company_page_company_type", "company_id", "page_type"),
        Index("idx_company_page_status", "status"),
        Index("idx_company_page_default", "company_id", "page_type", "is_default"),
        Index("idx_company_page_company_status", "company_id", "status"),
        Index("idx_company_page_published", "company_id", "status", "published_at"),
    )

    def __repr__(self) -> str:
        return f"<CompanyPageModel(id='{self.id}', company_id='{self.company_id}', page_type='{self.page_type}', status='{self.status}')>"
