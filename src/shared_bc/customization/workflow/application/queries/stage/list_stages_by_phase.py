"""List Stages by Phase Query."""
from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.shared_bc.customization.workflow.application.mappers.workflow_stage_mapper import WorkflowStageMapper
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


@dataclass(frozen=True)
class ListStagesByPhaseQuery(Query):
    """Query to list all stages for a specific phase."""
    phase_id: PhaseId
    workflow_type: WorkflowTypeEnum


class ListStagesByPhaseQueryHandler(QueryHandler[ListStagesByPhaseQuery, List[WorkflowStageDto]]):
    """Handler for listing stages by phase."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListStagesByPhaseQuery) -> List[WorkflowStageDto]:
        """Handle the query."""
        stages = self._repository.list_by_phase(query.phase_id, query.workflow_type)
        
        return [WorkflowStageMapper.entity_to_dto(stage) for stage in stages]
