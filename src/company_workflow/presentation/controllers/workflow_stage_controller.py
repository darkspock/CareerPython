"""Workflow Stage Controller."""
import ulid
from typing import List, Optional

from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.company_workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.company_workflow.application.commands.create_stage_command import CreateStageCommand
from src.company_workflow.application.commands.update_stage_command import UpdateStageCommand
from src.company_workflow.application.commands.delete_stage_command import DeleteStageCommand
from src.company_workflow.application.commands.reorder_stages_command import ReorderStagesCommand
from src.company_workflow.application.commands.activate_stage_command import ActivateStageCommand
from src.company_workflow.application.commands.deactivate_stage_command import DeactivateStageCommand
from src.company_workflow.application.queries.get_stage_by_id import GetStageByIdQuery
from src.company_workflow.application.queries.list_stages_by_workflow import ListStagesByWorkflowQuery
from src.company_workflow.application.queries.get_initial_stage import GetInitialStageQuery
from src.company_workflow.application.queries.get_final_stages import GetFinalStagesQuery
from src.company_workflow.presentation.schemas.create_stage_request import CreateStageRequest
from src.company_workflow.presentation.schemas.update_stage_request import UpdateStageRequest
from src.company_workflow.presentation.schemas.reorder_stages_request import ReorderStagesRequest
from src.company_workflow.presentation.schemas.workflow_stage_response import WorkflowStageResponse
from src.company_workflow.presentation.mappers.workflow_stage_mapper import WorkflowStageResponseMapper


class WorkflowStageController:
    """Controller for workflow stage operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_stage(self, request: CreateStageRequest) -> WorkflowStageResponse:
        """Create a new workflow stage."""
        stage_id = str(ulid.new())

        command = CreateStageCommand(
            id=stage_id,
            workflow_id=request.workflow_id,
            name=request.name,
            description=request.description,
            stage_type=request.stage_type,
            order=request.order,
            required_outcome=request.required_outcome,
            estimated_duration_days=request.estimated_duration_days,
            is_active=request.is_active
        )

        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after creation")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def get_stage_by_id(self, stage_id: str) -> Optional[WorkflowStageResponse]:
        """Get a stage by ID."""
        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            return None

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def list_stages_by_workflow(self, workflow_id: str) -> List[WorkflowStageResponse]:
        """List all stages for a workflow."""
        query = ListStagesByWorkflowQuery(workflow_id=workflow_id)
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def get_initial_stage(self, workflow_id: str) -> Optional[WorkflowStageResponse]:
        """Get the initial stage of a workflow."""
        query = GetInitialStageQuery(workflow_id=workflow_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            return None

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def get_final_stages(self, workflow_id: str) -> List[WorkflowStageResponse]:
        """Get all final stages of a workflow."""
        query = GetFinalStagesQuery(workflow_id=workflow_id)
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_stage(self, stage_id: str, request: UpdateStageRequest) -> WorkflowStageResponse:
        """Update stage information."""
        command = UpdateStageCommand(
            id=stage_id,
            name=request.name,
            description=request.description,
            stage_type=request.stage_type,
            required_outcome=request.required_outcome,
            estimated_duration_days=request.estimated_duration_days
        )

        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after update")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def delete_stage(self, stage_id: str) -> None:
        """Delete a stage."""
        command = DeleteStageCommand(id=stage_id)
        self._command_bus.dispatch(command)

    def reorder_stages(self, workflow_id: str, request: ReorderStagesRequest) -> List[WorkflowStageResponse]:
        """Reorder stages in a workflow."""
        command = ReorderStagesCommand(
            workflow_id=workflow_id,
            stage_ids_in_order=request.stage_ids_in_order
        )

        self._command_bus.dispatch(command)

        query = ListStagesByWorkflowQuery(workflow_id=workflow_id)
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def activate_stage(self, stage_id: str) -> WorkflowStageResponse:
        """Activate a stage."""
        command = ActivateStageCommand(id=stage_id)
        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after activation")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def deactivate_stage(self, stage_id: str) -> WorkflowStageResponse:
        """Deactivate a stage."""
        command = DeactivateStageCommand(id=stage_id)
        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after deactivation")

        return WorkflowStageResponseMapper.dto_to_response(dto)
