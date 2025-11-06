from dataclasses import dataclass
from typing import List, Optional

from src.workflow.application.dtos.workflow_dto import WorkflowDto
from src.workflow.application.mappers.candidate_application_workflow_mapper import WorkflowMapper
from src.workflow.domain.infrastructure.candidate_application_workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.workflow.domain.enums.workflow_status_enum import WorkflowStatusEnum
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListWorkflowsByPhaseQuery(Query):
    """Query to list workflows filtered by phase and optionally status"""
    phase_id: str
    status: Optional[str] = None  # If None, returns all statuses


class ListWorkflowsByPhaseQueryHandler(QueryHandler[ListWorkflowsByPhaseQuery, List[WorkflowDto]]):
    def __init__(self, repository: WorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByPhaseQuery) -> List[WorkflowDto]:
        phase_id = PhaseId.from_string(query.phase_id)

        # Get workflows for this phase (repository filters by ACTIVE status)
        workflows = self._repository.list_by_phase_id(phase_id.value)

        # If status filter is provided and it's not ACTIVE, filter further
        if query.status and query.status.upper() != WorkflowStatusEnum.ACTIVE.value:
            try:
                status_enum = WorkflowStatusEnum[query.status.upper()]
                workflows = [w for w in workflows if w.status == status_enum]
            except KeyError:
                # Invalid status, return empty list
                return []

        return [WorkflowMapper.entity_to_dto(w) for w in workflows]
