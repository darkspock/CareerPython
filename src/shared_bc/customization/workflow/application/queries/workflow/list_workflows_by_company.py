from dataclasses import dataclass
from typing import List, Optional

from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.mappers.workflow_mapper import WorkflowMapper
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface


@dataclass(frozen=True)
class ListWorkflowsByCompanyQuery(Query):
    """Query to list all workflows for a company"""
    company_id: CompanyId
    workflow_type: Optional[WorkflowTypeEnum] = None


class ListWorkflowsByCompanyQueryHandler(QueryHandler[ListWorkflowsByCompanyQuery, List[WorkflowDto]]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByCompanyQuery) -> List[WorkflowDto]:
        workflows = self._repository.list_by_company(query.company_id, query.workflow_type)
        return [WorkflowMapper.entity_to_dto(w) for w in workflows]
