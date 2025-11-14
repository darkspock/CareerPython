"""
Get Company Page By ID Query Handler - Handler para obtener página por ID
"""
from typing import Optional

from src.company_bc.company_page.domain.value_objects.page_id import PageId
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_bc.company_page.application.dtos.company_page_dto import CompanyPageDto
from src.company_bc.company_page.application.mappers.company_page_mapper import CompanyPageMapper
from src.company_bc.company_page.application.queries.get_company_page_by_id_query import GetCompanyPageByIdQuery
from src.framework.application.query_bus import QueryHandler


class GetCompanyPageByIdQueryHandler(QueryHandler[GetCompanyPageByIdQuery, Optional[CompanyPageDto]]):
    """Handler para obtener una página de empresa por ID"""
    
    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository
    
    def handle(self, query: GetCompanyPageByIdQuery) -> Optional[CompanyPageDto]:
        """Manejar query de obtener página por ID"""
        
        # Buscar página
        page_id = PageId(query.page_id)
        page = self.repository.get_by_id(page_id)
        
        # Convertir a DTO si existe
        return CompanyPageMapper.entity_to_dto(page) if page else None
