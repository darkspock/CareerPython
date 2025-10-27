from dataclasses import dataclass
from typing import List, Optional

from src.company_workflow.application.dtos.company_workflow_dto import CompanyWorkflowDto
from src.company_workflow.application.mappers.company_workflow_mapper import CompanyWorkflowMapper
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import \
    CompanyWorkflowRepositoryInterface
from src.company_workflow.domain.enums.workflow_status import WorkflowStatus
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListWorkflowsByPhaseQuery(Query):
    """Query to list workflows filtered by phase and optionally status"""
    phase_id: str
    status: Optional[str] = None  # If None, returns all statuses


class ListWorkflowsByPhaseQueryHandler(QueryHandler[ListWorkflowsByPhaseQuery, List[CompanyWorkflowDto]]):
    def __init__(self, repository: CompanyWorkflowRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListWorkflowsByPhaseQuery) -> List[CompanyWorkflowDto]:
        phase_id = PhaseId.from_string(query.phase_id)

        # Get workflows for this phase (repository filters by ACTIVE status)
        workflows = self._repository.list_by_phase_id(phase_id.value)

        # If status filter is provided and it's not ACTIVE, filter further
        if query.status and query.status.upper() != WorkflowStatus.ACTIVE.value:
            try:
                status_enum = WorkflowStatus[query.status.upper()]
                workflows = [w for w in workflows if w.status == status_enum]
            except KeyError:
                # Invalid status, return empty list
                return []

        return [CompanyWorkflowMapper.entity_to_dto(w) for w in workflows]
