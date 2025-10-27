"""List phases by company query"""
from dataclasses import dataclass
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.application.queries.get_phase_by_id_query import PhaseDto
from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface


@dataclass
class ListPhasesByCompanyQuery:
    """Query to list all phases for a company"""
    company_id: CompanyId


class ListPhasesByCompanyQueryHandler:
    """Handler for ListPhasesByCompanyQuery"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def handle(self, query: ListPhasesByCompanyQuery) -> List[PhaseDto]:
        """Handle the query to list phases for a company"""
        phases = self.phase_repository.list_by_company(query.company_id)

        return [PhaseDto.from_entity(phase) for phase in phases]
