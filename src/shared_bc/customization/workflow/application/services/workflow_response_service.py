"""Workflow Response Service - Service for obtaining enriched WorkflowResponse"""
from typing import Optional

from adapters.http.shared.workflow.mappers.workflow_mapper import WorkflowResponseMapper
from adapters.http.shared.workflow.mappers.workflow_stage_mapper import WorkflowStageResponseMapper
from adapters.http.shared.workflow.schemas.workflow_response import WorkflowResponse
from src.framework.application.query_bus import QueryBus
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_workflow import \
    ListStagesByWorkflowQuery
from src.shared_bc.customization.workflow.application.queries.workflow.get_workflow_by_id import GetWorkflowByIdQuery
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


class WorkflowResponseService:
    """Service for obtaining enriched WorkflowResponse with stages"""

    def __init__(self, query_bus: QueryBus):
        self._query_bus = query_bus

    def get_enriched_workflow(self, workflow_id: WorkflowId) -> WorkflowResponse:
        """
        Get an enriched WorkflowResponse with stages for a given workflow ID.
        
        Args:
            workflow_id: WorkflowId value object (not string)
            
        Returns:
            WorkflowResponse: Enriched workflow response with stages
            
        Raises:
            ValueError: If workflow is not found
        """
        # Get workflow DTO
        query = GetWorkflowByIdQuery(id=workflow_id)
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise ValueError(f"Workflow with ID {workflow_id.value} not found")

        # Convert to response
        response = WorkflowResponseMapper.dto_to_response(dto)

        # Enrich with stages
        stages_query = ListStagesByWorkflowQuery(workflow_id=workflow_id)
        stage_dtos: list[WorkflowStageDto] = self._query_bus.query(stages_query)
        response.stages = [
            WorkflowStageResponseMapper.dto_to_response(stage_dto).model_dump()
            for stage_dto in stage_dtos
        ]

        return response
