"""
Get Public Company Page Query Handler - Handler para obtener página pública
"""
from typing import Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company_page.application.dtos.company_page_dto import CompanyPageDto
from src.company_bc.company_page.application.mappers.company_page_mapper import CompanyPageMapper
from src.company_bc.company_page.application.queries.get_public_company_page_query import GetPublicCompanyPageQuery
from src.company_bc.company_page.domain.enums.page_type import PageType
from src.company_bc.company_page.domain.infrastructure.company_page_repository_interface import \
    CompanyPageRepositoryInterface
from src.framework.application.query_bus import QueryHandler


class GetPublicCompanyPageQueryHandler(QueryHandler[GetPublicCompanyPageQuery, Optional[CompanyPageDto]]):
    """Handler para obtener una página pública de empresa"""

    def __init__(self, repository: CompanyPageRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetPublicCompanyPageQuery) -> Optional[CompanyPageDto]:
        """Manejar query de obtener página pública"""

        # Convertir strings a value objects
        company_id = CompanyId(query.company_id)
        page_type = PageType(query.page_type)

        # Buscar página por defecto del tipo especificado
        page = self.repository.get_default_by_type(company_id, page_type)

        # Si no hay página por defecto, buscar cualquier página del tipo
        if not page:
            page = self.repository.get_by_company_and_type(company_id, page_type)

        # Solo retornar si la página está publicada
        if page and page.is_publicly_visible():
            return CompanyPageMapper.entity_to_dto(page)

        return None
