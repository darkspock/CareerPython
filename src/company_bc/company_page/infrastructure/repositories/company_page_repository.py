"""
Company Page Repository - Implementación del repositorio de páginas de empresa
"""

from typing import Optional, List, Any

from sqlalchemy import and_

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company_page.application.mappers.company_page_mapper import CompanyPageMapper
from src.company_bc.company_page.domain.entities.company_page import CompanyPage
from src.company_bc.company_page.domain.enums.page_status import PageStatus
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.exceptions.company_page_exceptions import (
    PageTypeAlreadyExistsException,
    PageNotFoundException
)
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import \
    CompanyPageRepositoryInterface
from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.company_bc.company_page.infrastructure.models.company_page_model import CompanyPageModel


class CompanyPageRepository(CompanyPageRepositoryInterface):
    """Implementación del repositorio de páginas de empresa"""

    def __init__(self, database: Any):
        self.database = database

    def save(self, page: CompanyPage) -> None:
        """Guardar una página de empresa"""
        session = self.database.get_session()
        try:
            # Verificar si ya existe una página del mismo tipo para la empresa
            existing_page = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == page.company_id.value,
                    CompanyPageModel.page_type == page.page_type.value,
                    CompanyPageModel.id != page.id.value
                )
            ).first()

            if existing_page:
                raise PageTypeAlreadyExistsException(
                    company_id=page.company_id.value,
                    page_type=page.page_type.value
                )

            # Buscar si ya existe el modelo
            existing_model = session.query(CompanyPageModel).filter(
                CompanyPageModel.id == page.id.value
            ).first()

            if existing_model:
                # Actualizar modelo existente
                self._update_model(existing_model, page)
            else:
                # Crear nuevo modelo
                model = CompanyPageMapper.entity_to_model(page)
                session.add(model)

            session.commit()

        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()

    def get_by_id(self, page_id: PageId) -> Optional[CompanyPage]:
        """Obtener página por ID"""
        session = self.database.get_session()
        try:
            model = session.query(CompanyPageModel).filter(
                CompanyPageModel.id == page_id.value
            ).first()

            return CompanyPageMapper.model_to_entity(model) if model else None
        finally:
            session.close()

    def get_by_company_and_type(
            self,
            company_id: CompanyId,
            page_type: PageType
    ) -> Optional[CompanyPage]:
        """Obtener página por empresa y tipo"""
        session = self.database.get_session()
        try:
            model = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.page_type == page_type.value
                )
            ).first()

            return CompanyPageMapper.model_to_entity(model) if model else None
        finally:
            session.close()

    def list_by_company(self, company_id: CompanyId) -> List[CompanyPage]:
        """Listar todas las páginas de una empresa"""
        session = self.database.get_session()
        try:
            models = session.query(CompanyPageModel).filter(
                CompanyPageModel.company_id == company_id.value
            ).order_by(CompanyPageModel.created_at.desc()).all()

            return CompanyPageMapper.models_to_entities(models)
        finally:
            session.close()

    def list_by_company_and_status(
            self,
            company_id: CompanyId,
            status: PageStatus
    ) -> List[CompanyPage]:
        """Listar páginas de una empresa por estado"""
        session = self.database.get_session()
        try:
            models = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.status == status.value
                )
            ).order_by(CompanyPageModel.created_at.desc()).all()

            return CompanyPageMapper.models_to_entities(models)
        finally:
            session.close()

    def list_by_company_and_type(
            self,
            company_id: CompanyId,
            page_type: PageType
    ) -> List[CompanyPage]:
        """Listar páginas de una empresa por tipo"""
        session = self.database.get_session()
        try:
            models = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.page_type == page_type.value
                )
            ).order_by(CompanyPageModel.created_at.desc()).all()

            return CompanyPageMapper.models_to_entities(models)
        finally:
            session.close()

    def list_by_company_type_and_status(
            self,
            company_id: CompanyId,
            page_type: PageType,
            status: PageStatus
    ) -> List[CompanyPage]:
        """Listar páginas de una empresa por tipo y estado"""
        session = self.database.get_session()
        try:
            models = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.page_type == page_type.value,
                    CompanyPageModel.status == status.value
                )
            ).order_by(CompanyPageModel.created_at.desc()).all()

            return CompanyPageMapper.models_to_entities(models)
        finally:
            session.close()

    def get_default_by_type(
            self,
            company_id: CompanyId,
            page_type: PageType
    ) -> Optional[CompanyPage]:
        """Obtener página por defecto de un tipo específico"""
        session = self.database.get_session()
        try:
            model = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.page_type == page_type.value,
                    CompanyPageModel.is_default.is_(True)
                )
            ).first()

            return CompanyPageMapper.model_to_entity(model) if model else None
        finally:
            session.close()

    def list_public_pages(self, company_id: CompanyId) -> List[CompanyPage]:
        """Listar páginas públicas de una empresa"""
        session = self.database.get_session()
        try:
            models = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.status == PageStatus.PUBLISHED.value
                )
            ).order_by(CompanyPageModel.created_at.desc()).all()

            return CompanyPageMapper.models_to_entities(models)
        finally:
            session.close()

    def delete(self, page_id: PageId) -> None:
        """Eliminar una página"""
        session = self.database.get_session()
        try:
            model = session.query(CompanyPageModel).filter(
                CompanyPageModel.id == page_id.value
            ).first()

            if not model:
                raise PageNotFoundException(page_id.value)

            session.delete(model)
            session.commit()
        finally:
            session.close()

    def exists_by_company_and_type(
            self,
            company_id: CompanyId,
            page_type: PageType
    ) -> bool:
        """Verificar si existe una página del tipo especificado para la empresa"""
        session = self.database.get_session()
        try:
            count = session.query(CompanyPageModel).filter(
                and_(
                    CompanyPageModel.company_id == company_id.value,
                    CompanyPageModel.page_type == page_type.value
                )
            ).count()

            return bool(count > 0)
        finally:
            session.close()

    def count_by_company(self, company_id: CompanyId) -> int:
        """Contar páginas de una empresa"""
        session = self.database.get_session()
        try:
            return int(session.query(CompanyPageModel).filter(
                CompanyPageModel.company_id == company_id.value
            ).count())
        finally:
            session.close()

    def _update_model(self, model: CompanyPageModel, entity: CompanyPage) -> None:
        """Actualizar modelo existente con datos de la entidad"""
        model.company_id = entity.company_id.value
        model.page_type = entity.page_type.value
        model.title = entity.title
        model.html_content = entity.content.html_content
        model.plain_text = entity.content.plain_text
        model.word_count = entity.content.word_count
        model.meta_description = entity.metadata.description
        model.meta_keywords = entity.metadata.keywords
        model.language = entity.metadata.language
        model.status = entity.status.value
        model.is_default = entity.is_default
        model.version = entity.version
        model.updated_at = entity.updated_at
        model.published_at = entity.published_at
