"""Get Initial Stage Query and Handler."""
from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.workflow.application.mappers.workflow_stage_mapper import WorkflowStageMapper
from src.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class GetInitialStageQuery(Query):
    """Query to get the initial stage of a workflow."""
    workflow_id: WorkflowId


class GetInitialStageQueryHandler(QueryHandler[GetInitialStageQuery, Optional[WorkflowStageDto]]):
    """Handler for getting the initial stage of a workflow."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetInitialStageQuery) -> Optional[WorkflowStageDto]:
        """
        Handle the get initial stage query.

        Args:
            query: The get initial stage query

        Returns:
            WorkflowStageDto if found, None otherwise
        """
        stage = self.repository.get_initial_stage(query.workflow_id)

        if not stage:
            return None

        return WorkflowStageMapper.entity_to_dto(stage)
