"""Get Final Stages Query and Handler."""
from dataclasses import dataclass
from typing import List

from src.shared.application.query_bus import Query, QueryHandler
from src.company_workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.company_workflow.application.mappers.workflow_stage_mapper import WorkflowStageMapper
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId


@dataclass(frozen=True)
class GetFinalStagesQuery(Query):
    """Query to get all final stages of a workflow."""
    workflow_id: str


class GetFinalStagesQueryHandler(QueryHandler[GetFinalStagesQuery, List[WorkflowStageDto]]):
    """Handler for getting all final stages of a workflow."""

    def __init__(self, repository: WorkflowStageRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetFinalStagesQuery) -> List[WorkflowStageDto]:
        """
        Handle the get final stages query.

        Args:
            query: The get final stages query

        Returns:
            List of WorkflowStageDto for final stages
        """
        workflow_id = CompanyWorkflowId.from_string(query.workflow_id)
        stages = self.repository.get_final_stages(workflow_id)

        return [WorkflowStageMapper.entity_to_dto(stage) for stage in stages]
