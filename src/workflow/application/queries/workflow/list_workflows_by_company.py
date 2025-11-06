from dataclasses import dataclass
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.workflow.application.dtos.workflow_dto import WorkflowDto
from src.workflow.application.mappers.workflow_mapper import WorkflowMapper
from src.shared.application.query_bus import Query, QueryHandler
from src.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface


@dataclass(frozen=True)
class ListWorkflowsByCompanyQuery(Query):
    """Query to list all workflows for a company"""
    company_id: CompanyId
    workflow_type: WorkflowTypeEnum


class ListWorkflowsByCompanyQueryHandler(QueryHandler[ListWorkflowsByCompanyQuery, List[WorkflowDto]]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByCompanyQuery) -> List[WorkflowDto]:
        workflows = self._repository.list_by_company(query.company_id, query.workflow_type)
        return [WorkflowMapper.entity_to_dto(w) for w in workflows]
