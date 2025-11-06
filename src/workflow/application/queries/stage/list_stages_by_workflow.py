"""List Stages By Workflow Query and Handler."""
from dataclasses import dataclass
from typing import List

from src.shared.application.query_bus import Query, QueryHandler
from src.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.workflow.application.mappers.workflow_stage_mapper import WorkflowStageMapper
from src.workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass(frozen=True)
class ListStagesByWorkflowQuery(Query):
    """Query to list all stages for a workflow."""
    workflow_id: str


class ListStagesByWorkflowQueryHandler(QueryHandler[ListStagesByWorkflowQuery, List[WorkflowStageDto]]):
    """Handler for listing all stages for a workflow."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListStagesByWorkflowQuery) -> List[WorkflowStageDto]:
        """
        Handle the list stages by workflow query.

        Args:
            query: The list stages by workflow query

        Returns:
            List of WorkflowStageDto
        """
        workflow_id = WorkflowId.from_string(query.workflow_id)
        stages = self.repository.list_by_workflow(workflow_id)

        return [WorkflowStageMapper.entity_to_dto(stage) for stage in stages]
