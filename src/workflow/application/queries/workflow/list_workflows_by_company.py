from dataclasses import dataclass
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.workflow.application.dtos.workflow_dto import WorkflowDto
from src.workflow.application.mappers.candidate_application_workflow_mapper import WorkflowMapper
from src.workflow.domain.infrastructure.candidate_application_workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListWorkflowsByCompanyQuery(Query):
    """Query to list all workflows for a company"""
    company_id: str


class ListWorkflowsByCompanyQueryHandler(QueryHandler[ListWorkflowsByCompanyQuery, List[WorkflowDto]]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByCompanyQuery) -> List[WorkflowDto]:
        company_id = CompanyId.from_string(query.company_id)
        workflows = self._repository.list_by_company(company_id)
        return [WorkflowMapper.entity_to_dto(w) for w in workflows]
