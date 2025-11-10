"""
List Company Pages Query Handler - Handler para listar páginas de empresa
"""
from typing import List

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company_page.domain.enums.page_status import PageStatus
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.company_bc.company_page.application.dtos.company_page_dto import CompanyPageDto
from src.company_bc.company_page.application.mappers.company_page_mapper import CompanyPageMapper
from src.company_bc.company_page.application.queries.list_company_pages_query import ListCompanyPagesQuery
from src.framework.application.query_bus import QueryHandler


class ListCompanyPagesQueryHandler(QueryHandler[ListCompanyPagesQuery, List[CompanyPageDto]]):
    """Handler para listar páginas de una empresa"""
    
    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository
    
    def handle(self, query: ListCompanyPagesQuery) -> List[CompanyPageDto]:
        """Manejar query de listar páginas"""
        
        # Convertir string a value object
        company_id = CompanyId(query.company_id)
        
        # Listar páginas según filtros
        if query.page_type and query.status:
            page_type = PageType(query.page_type)
            status = PageStatus(query.status)
            pages = self.repository.list_by_company_type_and_status(company_id, page_type, status)
        elif query.page_type:
            page_type = PageType(query.page_type)
            pages = self.repository.list_by_company_and_type(company_id, page_type)
        elif query.status:
            status = PageStatus(query.status)
            pages = self.repository.list_by_company_and_status(company_id, status)
        else:
            pages = self.repository.list_by_company(company_id)
        
        # Convertir a DTOs
        return CompanyPageMapper.entities_to_dtos(pages)
