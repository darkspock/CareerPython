from dataclasses import dataclass
from typing import Optional

from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.mappers.workflow_mapper import WorkflowMapper
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetWorkflowByIdQuery(Query):
    """Query to get a workflow by ID"""
    id: WorkflowId


class GetWorkflowByIdQueryHandler(QueryHandler[GetWorkflowByIdQuery, Optional[WorkflowDto]]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetWorkflowByIdQuery) -> Optional[WorkflowDto]:
        workflow = self._repository.get_by_id(query.id)
        if not workflow:
            return None
        return WorkflowMapper.entity_to_dto(workflow)
