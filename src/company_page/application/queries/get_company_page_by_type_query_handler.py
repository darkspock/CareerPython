"""
Get Company Page By Type Query Handler - Handler para obtener página por tipo
"""
from typing import Optional

from src.company.domain.value_objects.company_id import CompanyId
from src.company_page.application.dtos.company_page_dto import CompanyPageDto
from src.company_page.application.mappers.company_page_mapper import CompanyPageMapper
from src.company_page.application.queries.get_company_page_by_type_query import GetCompanyPageByTypeQuery
from src.company_page.domain.enums.page_type import PageType
from src.company_page.domain.infrastructure.company_page_repository_interface import CompanyPageRepositoryInterface
from src.shared.application.query_bus import QueryHandler


class GetCompanyPageByTypeQueryHandler(QueryHandler[GetCompanyPageByTypeQuery, Optional[CompanyPageDto]]):
    """Handler para obtener una página de empresa por tipo"""

    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetCompanyPageByTypeQuery) -> Optional[CompanyPageDto]:
        """Manejar query de obtener página por tipo"""

        # Convertir strings a value objects
        company_id = CompanyId(query.company_id)
        page_type = PageType(query.page_type)

        # Buscar página
        page = self.repository.get_by_company_and_type(company_id, page_type)

        # Convertir a DTO si existe
        return CompanyPageMapper.entity_to_dto(page) if page else None
