"""
Company Page DTO - Data Transfer Object para páginas de empresa
"""
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.company_bc.company_page.domain.entities.company_page import CompanyPage


@dataclass
class CompanyPageDto:
    """DTO para transferencia de datos de páginas de empresa"""

    # Identifiers
    id: str
    company_id: str

    # Basic Fields
    page_type: str
    title: str

    # Content Fields
    html_content: str
    plain_text: str
    word_count: int

    # SEO Fields
    meta_description: Optional[str]
    meta_keywords: List[str]
    language: str

    # Status Fields
    status: str
    is_default: bool
    version: int

    # Timestamps
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    @classmethod
    def from_entity(cls, entity: CompanyPage) -> "CompanyPageDto":
        """Crear DTO desde entidad de dominio"""
        return cls(
            id=entity.id.value,
            company_id=entity.company_id.value,
            page_type=entity.page_type.value,
            title=entity.title,
            html_content=entity.content.html_content,
            plain_text=entity.content.plain_text,
            word_count=entity.content.word_count,
            meta_description=entity.metadata.description,
            meta_keywords=entity.metadata.keywords,
            language=entity.metadata.language,
            status=entity.status.value,
            is_default=entity.is_default,
            version=entity.version,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
            published_at=entity.published_at
        )
