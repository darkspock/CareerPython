"""
Company Page Mapper - Mappers para conversión entre capas
"""
from typing import List

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company_page.application.dtos.company_page_dto import CompanyPageDto
from src.company_bc.company_page.domain.entities.company_page import CompanyPage
from src.company_bc.company_page.domain.enums.page_status import PageStatus
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.value_objects.page_content import PageContent
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.company_bc.company_page.domain.value_objects.page_metadata import PageMetadata
from src.company_page.infrastructure.models.company_page_model import CompanyPageModel


class CompanyPageMapper:
    """Mapper para conversión entre entidades de dominio y modelos de infraestructura"""

    @staticmethod
    def entity_to_model(entity: CompanyPage) -> CompanyPageModel:
        """Convertir entidad de dominio a modelo SQLAlchemy"""
        return CompanyPageModel(
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

    @staticmethod
    def model_to_entity(model: CompanyPageModel) -> CompanyPage:
        """Convertir modelo SQLAlchemy a entidad de dominio"""
        # Crear value objects
        page_id = PageId(model.id)
        company_id = CompanyId(model.company_id)
        page_type = PageType(model.page_type)
        page_status = PageStatus(model.status)

        # Crear PageContent
        content = PageContent(
            html_content=model.html_content,
            plain_text=model.plain_text,
            word_count=model.word_count
        )

        # Crear PageMetadata
        metadata = PageMetadata(
            title=model.title,
            description=model.meta_description,
            keywords=model.meta_keywords or [],
            language=model.language
        )

        # Crear entidad
        return CompanyPage(
            id=page_id,
            company_id=company_id,
            page_type=page_type,
            title=model.title,
            content=content,
            metadata=metadata,
            status=page_status,
            is_default=model.is_default,
            version=model.version,
            created_at=model.created_at,
            updated_at=model.updated_at,
            published_at=model.published_at
        )

    @staticmethod
    def models_to_entities(models: List[CompanyPageModel]) -> List[CompanyPage]:
        """Convertir lista de modelos a lista de entidades"""
        return [CompanyPageMapper.model_to_entity(model) for model in models]

    @staticmethod
    def entity_to_dto(entity: CompanyPage) -> CompanyPageDto:
        """Convertir entidad de dominio a DTO"""
        return CompanyPageDto.from_entity(entity)

    @staticmethod
    def entities_to_dtos(entities: List[CompanyPage]) -> List[CompanyPageDto]:
        """Convertir lista de entidades a lista de DTOs"""
        return [CompanyPageMapper.entity_to_dto(entity) for entity in entities]
