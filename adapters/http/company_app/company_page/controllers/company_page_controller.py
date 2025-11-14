"""
Company Page Controller - Controller for company pages
"""
from typing import List, Optional

from adapters.http.company_app.company_page.schemas.company_page_request import CreateCompanyPageRequest, \
    UpdateCompanyPageRequest
from adapters.http.company_app.company_page.schemas.company_page_response import CompanyPageResponse, CompanyPageListResponse
from src.company_bc.company_page.application.commands.create_company_page_command import CreateCompanyPageCommand
from src.company_bc.company_page.application.commands.update_company_page_command import UpdateCompanyPageCommand
from src.company_bc.company_page.application.commands.publish_company_page_command import PublishCompanyPageCommand
from src.company_bc.company_page.application.commands.archive_company_page_command import ArchiveCompanyPageCommand
from src.company_bc.company_page.application.commands.set_default_page_command import SetDefaultPageCommand
from src.company_bc.company_page.application.commands.delete_company_page_command import DeleteCompanyPageCommand

from src.company_bc.company_page.application.queries.get_company_page_by_id_query import GetCompanyPageByIdQuery
from src.company_bc.company_page.application.queries.get_company_page_by_type_query import GetCompanyPageByTypeQuery
from src.company_bc.company_page.application.queries.list_company_pages_query import ListCompanyPagesQuery
from src.company_bc.company_page.application.queries.get_public_company_page_query import GetPublicCompanyPageQuery

from src.company_bc.company_page.application.dtos.company_page_dto import CompanyPageDto
# Note: Response schemas use plain strings, not domain enums

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus


class CompanyPageController:
    """Controller for company page management"""
    
    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus
    
    def create_page(self, company_id: str, request: CreateCompanyPageRequest) -> CompanyPageResponse:
        """Create a new company page"""
        
        # Crear comando
        command = CreateCompanyPageCommand(
            company_id=company_id,
            page_type=request.page_type.value,
            title=request.title,
            html_content=request.html_content,
            meta_description=request.meta_description,
            meta_keywords=request.meta_keywords,
            language=request.language,
            is_default=request.is_default
        )
        
        # Ejecutar comando
        self.command_bus.execute(command)
        
        # Buscar página creada por tipo
        query = GetCompanyPageByTypeQuery(
            company_id=company_id,
            page_type=request.page_type.value
        )
        
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        # Convertir DTO a Response
        if not page_dto:
            raise ValueError(f"Page not found")
        return self._dto_to_response(page_dto)
    
    def update_page(self, page_id: str, request: UpdateCompanyPageRequest) -> CompanyPageResponse:
        """Actualizar una página de empresa existente"""
        
        # Crear comando
        command = UpdateCompanyPageCommand(
            page_id=page_id,
            title=request.title,
            html_content=request.html_content,
            meta_description=request.meta_description,
            meta_keywords=request.meta_keywords
        )
        
        # Ejecutar comando
        self.command_bus.execute(command)
        
        # Buscar página actualizada
        query = GetCompanyPageByIdQuery(page_id=page_id)
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        # Convertir DTO a Response
        if not page_dto:
            raise ValueError(f"Page not found")
        return self._dto_to_response(page_dto)
    
    def get_page(self, page_id: str) -> CompanyPageResponse:
        """Obtener una página de empresa por ID"""
        
        query = GetCompanyPageByIdQuery(page_id=page_id)
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        if not page_dto:
            raise ValueError(f"Page with ID {page_id} not found")
        
        return self._dto_to_response(page_dto)
    
    def list_pages(self, company_id: str, page_type: Optional[str] = None, status: Optional[str] = None) -> CompanyPageListResponse:
        """Listar páginas de una empresa"""
        
        query = ListCompanyPagesQuery(company_id=company_id, page_type=page_type, status=status)
        page_dtos:List[CompanyPageDto] = self.query_bus.query(query)
        
        # Convertir DTOs a Responses
        pages = [self._dto_to_response(page_dto) for page_dto in page_dtos]
        
        return CompanyPageListResponse(
            pages=pages,
            total=len(pages)
        )
    
    def publish_page(self, page_id: str) -> CompanyPageResponse:
        """Publicar una página de empresa"""
        
        command = PublishCompanyPageCommand(page_id=page_id)
        self.command_bus.execute(command)
        
        # Buscar página publicada
        query = GetCompanyPageByIdQuery(page_id=page_id)
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        if not page_dto:
            raise ValueError(f"Page not found")
        return self._dto_to_response(page_dto)
    
    def archive_page(self, page_id: str) -> CompanyPageResponse:
        """Archivar una página de empresa"""
        
        command = ArchiveCompanyPageCommand(page_id=page_id)
        self.command_bus.execute(command)
        
        # Buscar página archivada
        query = GetCompanyPageByIdQuery(page_id=page_id)
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        if not page_dto:
            raise ValueError(f"Page not found")
        return self._dto_to_response(page_dto)
    
    def set_default_page(self, page_id: str) -> CompanyPageResponse:
        """Marcar una página como página por defecto"""
        
        command = SetDefaultPageCommand(page_id=page_id)
        self.command_bus.execute(command)
        
        # Buscar página marcada como default
        query = GetCompanyPageByIdQuery(page_id=page_id)
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        if not page_dto:
            raise ValueError(f"Page not found")
        return self._dto_to_response(page_dto)
    
    def delete_page(self, page_id: str) -> None:
        """Eliminar una página de empresa"""
        
        command = DeleteCompanyPageCommand(page_id=page_id)
        self.command_bus.execute(command)
    
    def get_public_page(self, company_id: str, page_type: str) -> CompanyPageResponse:
        """Obtener una página pública de empresa"""
        
        query = GetPublicCompanyPageQuery(
            company_id=company_id,
            page_type=page_type
        )
        
        page_dto:Optional[CompanyPageDto] = self.query_bus.query(query)
        
        if not page_dto:
            raise ValueError(f"Page not found")
        return self._dto_to_response(page_dto)
    
    def _dto_to_response(self, page_dto: CompanyPageDto) -> CompanyPageResponse:
        """Convertir DTO a Response"""
        return CompanyPageResponse(
            id=page_dto.id,
            company_id=page_dto.company_id,
            page_type=page_dto.page_type,
            title=page_dto.title,
            html_content=page_dto.html_content,
            plain_text=page_dto.plain_text,
            word_count=page_dto.word_count,
            meta_description=page_dto.meta_description,
            meta_keywords=page_dto.meta_keywords,
            language=page_dto.language,
            status=page_dto.status,
            is_default=page_dto.is_default,
            version=page_dto.version,
            created_at=page_dto.created_at,
            updated_at=page_dto.updated_at,
            published_at=page_dto.published_at
        )
