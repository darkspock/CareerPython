"""
Company Page Entity - Entidad principal para páginas de empresa
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company_page.domain.enums.page_status import PageStatus
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import (
    InvalidPageStatusTransitionException,
    PageAlreadyDefaultException
)
from src.company_bc.company_page.domain.value_objects.page_content import PageContent
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.company_bc.company_page.domain.value_objects.page_metadata import PageMetadata


@dataclass
class CompanyPage:
    """Entidad para páginas de empresa"""

    id: PageId
    company_id: CompanyId
    page_type: PageType
    title: str
    content: PageContent
    metadata: PageMetadata
    status: PageStatus
    is_default: bool  # Si es la página por defecto para este tipo
    version: int
    created_at: datetime
    updated_at: datetime
    published_at: Optional[datetime]

    @classmethod
    def create(
            cls,
            company_id: CompanyId,
            page_type: PageType,
            title: str,
            html_content: str,
            metadata: PageMetadata,
            is_default: bool = False
    ) -> "CompanyPage":
        """Factory method para crear una nueva página"""

        # Validar que el título no esté vacío
        if not title.strip():
            raise ValueError("Title cannot be empty")

        # Crear contenido
        content = PageContent.create(html_content)

        # Crear ID único
        page_id = PageId.generate()

        # Fecha actual
        now = datetime.now()

        return cls(
            id=page_id,
            company_id=company_id,
            page_type=page_type,
            title=title.strip(),
            content=content,
            metadata=metadata,
            status=PageStatus.DRAFT,
            is_default=is_default,
            version=1,
            created_at=now,
            updated_at=now,
            published_at=None
        )

    def update_content(
            self,
            title: str,
            html_content: str,
            metadata: PageMetadata
    ) -> "CompanyPage":
        """Actualizar contenido de la página"""

        if not title.strip():
            raise ValueError("Title cannot be empty")

        # Crear nuevo contenido
        new_content = PageContent.create(html_content)

        # Crear nueva instancia con contenido actualizado
        return CompanyPage(
            id=self.id,
            company_id=self.company_id,
            page_type=self.page_type,
            title=title.strip(),
            content=new_content,
            metadata=metadata,
            status=self.status,
            is_default=self.is_default,
            version=self.version + 1,
            created_at=self.created_at,
            updated_at=datetime.now(),
            published_at=self.published_at
        )

    def publish(self) -> "CompanyPage":
        """Publicar la página"""

        if self.status == PageStatus.PUBLISHED:
            return self  # Ya está publicada

        if self.status == PageStatus.ARCHIVED:
            raise InvalidPageStatusTransitionException(
                current_status=self.status.value,
                target_status=PageStatus.PUBLISHED.value
            )

        # Crear nueva instancia con estado publicado
        return CompanyPage(
            id=self.id,
            company_id=self.company_id,
            page_type=self.page_type,
            title=self.title,
            content=self.content,
            metadata=self.metadata,
            status=PageStatus.PUBLISHED,
            is_default=self.is_default,
            version=self.version,
            created_at=self.created_at,
            updated_at=datetime.now(),
            published_at=datetime.now()
        )

    def archive(self) -> "CompanyPage":
        """Archivar la página"""

        if self.status == PageStatus.ARCHIVED:
            return self  # Ya está archivada

        # Crear nueva instancia con estado archivado
        return CompanyPage(
            id=self.id,
            company_id=self.company_id,
            page_type=self.page_type,
            title=self.title,
            content=self.content,
            metadata=self.metadata,
            status=PageStatus.ARCHIVED,
            is_default=False,  # Una página archivada no puede ser default
            version=self.version,
            created_at=self.created_at,
            updated_at=datetime.now(),
            published_at=self.published_at
        )

    def set_as_default(self) -> "CompanyPage":
        """Marcar como página por defecto para su tipo"""

        if self.is_default:
            raise PageAlreadyDefaultException(self.id.value)

        if self.status != PageStatus.PUBLISHED:
            raise InvalidPageStatusTransitionException(
                current_status=self.status.value,
                target_status="default"
            )

        # Crear nueva instancia marcada como default
        return CompanyPage(
            id=self.id,
            company_id=self.company_id,
            page_type=self.page_type,
            title=self.title,
            content=self.content,
            metadata=self.metadata,
            status=self.status,
            is_default=True,
            version=self.version,
            created_at=self.created_at,
            updated_at=datetime.now(),
            published_at=self.published_at
        )

    def unset_as_default(self) -> "CompanyPage":
        """Desmarcar como página por defecto"""

        if not self.is_default:
            return self  # Ya no es default

        # Crear nueva instancia sin ser default
        return CompanyPage(
            id=self.id,
            company_id=self.company_id,
            page_type=self.page_type,
            title=self.title,
            content=self.content,
            metadata=self.metadata,
            status=self.status,
            is_default=False,
            version=self.version,
            created_at=self.created_at,
            updated_at=datetime.now(),
            published_at=self.published_at
        )

    def is_publicly_visible(self) -> bool:
        """Verificar si la página es visible públicamente"""
        return self.status == PageStatus.PUBLISHED

    def can_be_edited(self) -> bool:
        """Verificar si la página puede ser editada"""
        return self.status in [PageStatus.DRAFT, PageStatus.PUBLISHED]

    def can_be_published(self) -> bool:
        """Verificar si la página puede ser publicada"""
        return self.status == PageStatus.DRAFT

    def can_be_archived(self) -> bool:
        """Verificar si la página puede ser archivada"""
        return self.status in [PageStatus.DRAFT, PageStatus.PUBLISHED]
