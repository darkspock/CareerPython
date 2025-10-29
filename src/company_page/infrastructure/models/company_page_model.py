"""
Company Page Model - Modelo SQLAlchemy para páginas de empresa
"""
from sqlalchemy import (
    Column, String, Text, Integer, Boolean, DateTime, JSON, ForeignKey, Index
)
from sqlalchemy.orm import relationship

from core.base import Base
from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.enums.page_status import PageStatus


class CompanyPageModel(Base):
    """Modelo SQLAlchemy para páginas de empresa"""
    
    __tablename__ = "company_pages"
    
    # Primary Key
    id = Column(String(255), primary_key=True)
    
    # Foreign Keys
    company_id = Column(String(255), ForeignKey("companies.id"), nullable=False)
    
    # Basic Fields
    page_type = Column(String(50), nullable=False)  # Enum PageType
    title = Column(String(500), nullable=False)
    
    # Content Fields
    html_content = Column(Text, nullable=False)
    plain_text = Column(Text, nullable=False)
    word_count = Column(Integer, nullable=False)
    
    # SEO Fields
    meta_description = Column(Text)
    meta_keywords = Column(JSON)  # Array de strings
    language = Column(String(10), default="es")
    
    # Status Fields
    status = Column(String(50), nullable=False)  # Enum PageStatus
    is_default = Column(Boolean, default=False)
    version = Column(Integer, default=1)
    
    # Timestamps
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    published_at = Column(DateTime)
    
    # Relationships
    company = relationship("CompanyModel")
    
    # Indexes for performance
    __table_args__ = (
        Index("idx_company_page_company_type", "company_id", "page_type"),
        Index("idx_company_page_status", "status"),
        Index("idx_company_page_default", "company_id", "page_type", "is_default"),
        Index("idx_company_page_company_status", "company_id", "status"),
        Index("idx_company_page_published", "company_id", "status", "published_at"),
    )
    
    def __repr__(self):
        return f"<CompanyPageModel(id='{self.id}', company_id='{self.company_id}', page_type='{self.page_type}', status='{self.status}')>"
