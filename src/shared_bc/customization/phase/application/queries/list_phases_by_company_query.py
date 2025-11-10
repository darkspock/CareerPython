"""List phases by company query"""
from dataclasses import dataclass
from typing import List

from src.company_bc.company.domain.value_objects import CompanyId
from src.shared_bc.customization.phase.application.queries.get_phase_by_id_query import PhaseDto
from src.shared_bc.customization.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class ListPhasesByCompanyQuery(Query):
    """Query to list all phases for a company"""
    company_id: CompanyId


class ListPhasesByCompanyQueryHandler(QueryHandler[ListPhasesByCompanyQuery, List[PhaseDto]]):
    """Handler for ListPhasesByCompanyQuery"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def handle(self, query: ListPhasesByCompanyQuery) -> List[PhaseDto]:
        """Handle the query to list phases for a company"""
        phases = self.phase_repository.list_by_company(query.company_id)

        return [PhaseDto.from_entity(phase) for phase in phases]
