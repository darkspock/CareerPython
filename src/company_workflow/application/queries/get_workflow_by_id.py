from dataclasses import dataclass
from typing import Optional

from src.company_workflow.application.dtos.company_workflow_dto import CompanyWorkflowDto
from src.company_workflow.application.mappers.company_workflow_mapper import CompanyWorkflowMapper
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import \
    CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetWorkflowByIdQuery(Query):
    """Query to get a workflow by ID"""
    id: CompanyWorkflowId


class GetWorkflowByIdQueryHandler(QueryHandler[GetWorkflowByIdQuery, Optional[CompanyWorkflowDto]]):
    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetWorkflowByIdQuery) -> Optional[CompanyWorkflowDto]:
        workflow = self._repository.get_by_id(query.id)
        if not workflow:
            return None
        return CompanyWorkflowMapper.entity_to_dto(workflow)
