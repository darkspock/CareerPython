from dataclasses import dataclass
from typing import List, Optional

from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.mappers.workflow_mapper import WorkflowMapper
from src.shared_bc.customization.workflow.domain.enums.workflow_status_enum import WorkflowStatusEnum
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import WorkflowRepositoryInterface


@dataclass(frozen=True)
class ListWorkflowsByPhaseQuery(Query):
    """Query to list workflows filtered by phase and optionally workflow_type and status"""
    phase_id: PhaseId
    workflow_type: Optional[WorkflowTypeEnum] = None  # If None, returns all workflow types
    status: Optional[WorkflowStatusEnum] = None  # If None, returns all statuses


class ListWorkflowsByPhaseQueryHandler(QueryHandler[ListWorkflowsByPhaseQuery, List[WorkflowDto]]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByPhaseQuery) -> List[WorkflowDto]:
        # Convert status enum to string value if provided
        status_value = query.status.value if query.status else None
        
        # Get workflows for this phase, filtered by workflow_type and optionally by status
        workflows = self._repository.list_by_phase_id(
            query.phase_id,
            query.workflow_type,
            status_value
        )

        return [WorkflowMapper.entity_to_dto(w) for w in workflows]
