from dataclasses import dataclass
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.company_workflow.application.dtos.company_workflow_dto import CompanyWorkflowDto
from src.company_workflow.application.mappers.company_workflow_mapper import CompanyWorkflowMapper
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import \
    CompanyWorkflowRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListWorkflowsByCompanyQuery(Query):
    """Query to list all workflows for a company"""
    company_id: str


class ListWorkflowsByCompanyQueryHandler(QueryHandler[ListWorkflowsByCompanyQuery, List[CompanyWorkflowDto]]):
    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByCompanyQuery) -> List[CompanyWorkflowDto]:
        company_id = CompanyId.from_string(query.company_id)
        workflows = self._repository.list_by_company(company_id)
        return [CompanyWorkflowMapper.entity_to_dto(w) for w in workflows]
