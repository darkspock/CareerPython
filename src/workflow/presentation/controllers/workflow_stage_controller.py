"""Workflow Stage Controller."""
import ulid
from typing import List, Optional

from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.workflow.application.commands.stage.create_stage_command import CreateStageCommand
from src.workflow.application.commands.stage.update_stage_command import UpdateStageCommand
from src.workflow.application.commands.stage.delete_stage_command import DeleteStageCommand
from src.workflow.application.commands.stage.reorder_stages_command import ReorderStagesCommand
from src.workflow.application.commands.stage.activate_stage_command import ActivateStageCommand
from src.workflow.application.commands.stage.deactivate_stage_command import DeactivateStageCommand
from src.workflow.application.queries.stage.get_stage_by_id import GetStageByIdQuery
from src.workflow.application.queries.stage.list_stages_by_workflow import ListStagesByWorkflowQuery
from src.workflow.application.queries.stage.get_initial_stage import GetInitialStageQuery
from src.workflow.application.queries.stage.get_final_stages import GetFinalStagesQuery
from src.workflow.presentation.schemas.create_stage_request import CreateStageRequest
from src.workflow.presentation.schemas.update_stage_request import UpdateStageRequest
from src.workflow.presentation.schemas.reorder_stages_request import ReorderStagesRequest
from src.workflow.presentation.schemas.stage_style_request import UpdateStageStyleRequest
from src.workflow.presentation.schemas.workflow_stage_response import WorkflowStageResponse
from src.workflow.presentation.mappers.workflow_stage_mapper import WorkflowStageResponseMapper


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
            allow_skip=request.allow_skip,
            estimated_duration_days=request.estimated_duration_days,
            is_active=request.is_active,
            default_role_ids=request.default_role_ids,
            default_assigned_users=request.default_assigned_users,
            email_template_id=request.email_template_id,
            custom_email_text=request.custom_email_text,
            deadline_days=request.deadline_days,
            estimated_cost=request.estimated_cost,
            next_phase_id=request.next_phase_id  # Phase 12
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

    def list_stages_by_phase(self, phase_id: str) -> List[WorkflowStageResponse]:
        """List all stages for a phase."""
        from src.workflow.application.queries.stage.list_stages_by_phase import ListStagesByPhaseQuery
        
        query = ListStagesByPhaseQuery(phase_id=phase_id)
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
            allow_skip=request.allow_skip,
            estimated_duration_days=request.estimated_duration_days,
            default_role_ids=request.default_role_ids,
            default_assigned_users=request.default_assigned_users,
            email_template_id=request.email_template_id,
            custom_email_text=request.custom_email_text,
            deadline_days=request.deadline_days,
            estimated_cost=request.estimated_cost,
            next_phase_id=request.next_phase_id,  # Phase 12
            kanban_display=request.kanban_display
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

    def update_stage_style(self, stage_id: str, style_request: UpdateStageStyleRequest) -> WorkflowStageResponse:
        """Update the visual style of a workflow stage."""
        # First get the current stage
        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)
        
        if not dto:
            raise Exception("Stage not found")

        # Create update command with style changes
        updated_style = {
            **dto.style,
            **{k: v for k, v in style_request.dict().items() if v is not None}
        }

        command = UpdateStageCommand(
            id=stage_id,
            name=dto.name,
            description=dto.description,
            stage_type=dto.stage_type,
            allow_skip=dto.allow_skip,
            estimated_duration_days=dto.estimated_duration_days,
            default_role_ids=dto.default_role_ids,
            default_assigned_users=dto.default_assigned_users,
            email_template_id=dto.email_template_id,
            custom_email_text=dto.custom_email_text,
            deadline_days=dto.deadline_days,
            estimated_cost=dto.estimated_cost,
            next_phase_id=dto.next_phase_id,
            style=updated_style
        )
        self._command_bus.dispatch(command)

        # Return updated stage
        updated_query = GetStageByIdQuery(id=stage_id)
        updated_dto: Optional[WorkflowStageDto] = self._query_bus.query(updated_query)

        if not updated_dto:
            raise Exception("Stage not found after style update")

        return WorkflowStageResponseMapper.dto_to_response(updated_dto)
