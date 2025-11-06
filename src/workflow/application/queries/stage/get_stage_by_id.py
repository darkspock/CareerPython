"""Get Stage By ID Query and Handler."""
from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.workflow.application.mappers.workflow_stage_mapper import WorkflowStageMapper
from src.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass(frozen=True)
class GetStageByIdQuery(Query):
    """Query to get a workflow stage by ID."""
    id: WorkflowStageId


class GetStageByIdQueryHandler(QueryHandler[GetStageByIdQuery, Optional[WorkflowStageDto]]):
    """Handler for getting a workflow stage by ID."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetStageByIdQuery) -> Optional[WorkflowStageDto]:
        """
        Handle the get stage by ID query.

        Args:
            query: The get stage by ID query

        Returns:
            WorkflowStageDto if found, None otherwise
        """
        stage = self.repository.get_by_id(query.id)

        if not stage:
            return None

        return WorkflowStageMapper.entity_to_dto(stage)
