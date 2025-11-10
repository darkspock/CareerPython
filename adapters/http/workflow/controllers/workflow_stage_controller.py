"""Workflow Stage Controller."""
from typing import List, Optional

from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.shared_bc.customization.workflow.application import WorkflowStageDto
from src.shared_bc.customization.workflow.application import CreateStageCommand
from src.shared_bc.customization.workflow.application.commands.stage.update_stage_command import UpdateStageCommand
from src.shared_bc.customization.workflow.application.commands.stage.delete_stage_command import DeleteStageCommand
from src.shared_bc.customization.workflow.application import ReorderStagesCommand
from src.shared_bc.customization.workflow.application.commands.stage.activate_stage_command import ActivateStageCommand
from src.shared_bc.customization.workflow.application import DeactivateStageCommand
from src.shared_bc.customization.workflow.application.queries.stage.get_stage_by_id import GetStageByIdQuery
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_workflow import ListStagesByWorkflowQuery
from src.shared_bc.customization.workflow.application import GetInitialStageQuery
from src.shared_bc.customization.workflow.application.queries.stage.get_final_stages import GetFinalStagesQuery
from adapters.http.workflow.schemas.create_stage_request import CreateStageRequest
from adapters.http.workflow.schemas.update_stage_request import UpdateStageRequest
from adapters.http.workflow.schemas.reorder_stages_request import ReorderStagesRequest
from adapters.http.workflow.schemas.stage_style_request import UpdateStageStyleRequest
from adapters.http.workflow.schemas.workflow_stage_response import WorkflowStageResponse
from adapters.http.workflow.mappers.workflow_stage_mapper import WorkflowStageResponseMapper
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
from src.shared_bc.customization.workflow.domain.enums.kanban_display_enum import KanbanDisplayEnum
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_style import WorkflowStageStyle
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


class WorkflowStageController:
    """Controller for workflow stage operations."""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_stage(self, request: CreateStageRequest) -> WorkflowStageResponse:
        """Create a new workflow stage."""
        stage_id = WorkflowStageId.generate()

        # Convert style dict to WorkflowStageStyle if provided
        style = None
        if request.style:
            style = WorkflowStageStyle(
                background_color=request.style.get("background_color", "#ffffff"),
                text_color=request.style.get("text_color", "#000000"),
                icon=request.style.get("icon", "")
            )

        command = CreateStageCommand(
            id=stage_id,
            workflow_id=WorkflowId.from_string(request.workflow_id),
            name=request.name,
            description=request.description,
            stage_type=WorkflowStageTypeEnum(request.stage_type),
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
            next_phase_id=PhaseId.from_string(request.next_phase_id) if request.next_phase_id else None,  # Phase 12
            kanban_display=KanbanDisplayEnum(request.kanban_display) if request.kanban_display else KanbanDisplayEnum.COLUMN,
            style=style,
            validation_rules=request.validation_rules,
            recommended_rules=request.recommended_rules
        )

        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after creation")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def get_stage_by_id(self, stage_id: str) -> Optional[WorkflowStageResponse]:
        """Get a stage by ID."""
        query = GetStageByIdQuery(id=WorkflowStageId.from_string(stage_id))
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            return None

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def list_stages_by_workflow(self, workflow_id: str) -> List[WorkflowStageResponse]:
        """List all stages for a workflow."""
        query = ListStagesByWorkflowQuery(workflow_id=WorkflowId.from_string(workflow_id))
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def list_stages_by_phase(self, phase_id: str, workflow_type: str) -> List[WorkflowStageResponse]:
        """List all stages for a phase."""
        from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_phase import ListStagesByPhaseQuery
        from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
        
        query = ListStagesByPhaseQuery(
            phase_id=PhaseId.from_string(phase_id),
            workflow_type=WorkflowTypeEnum(workflow_type)
        )
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def get_initial_stage(self, workflow_id: str) -> Optional[WorkflowStageResponse]:
        """Get the initial stage of a workflow."""
        query = GetInitialStageQuery(workflow_id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            return None

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def get_final_stages(self, workflow_id: str) -> List[WorkflowStageResponse]:
        """Get all final stages of a workflow."""
        query = GetFinalStagesQuery(workflow_id=WorkflowId.from_string(workflow_id))
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_stage(self, stage_id: str, request: UpdateStageRequest) -> WorkflowStageResponse:
        """Update stage information."""
        stage_id_vo = WorkflowStageId.from_string(stage_id)
        
        # Convert style dict to WorkflowStageStyle if provided
        style = None
        if request.style:
            style = WorkflowStageStyle(
                background_color=request.style.get("background_color", "#ffffff"),
                text_color=request.style.get("text_color", "#000000"),
                icon=request.style.get("icon", "")
            )

        command = UpdateStageCommand(
            id=stage_id_vo,
            name=request.name,
            description=request.description,
            stage_type=WorkflowStageTypeEnum(request.stage_type),
            allow_skip=request.allow_skip,
            estimated_duration_days=request.estimated_duration_days,
            default_role_ids=request.default_role_ids,
            default_assigned_users=request.default_assigned_users,
            email_template_id=request.email_template_id,
            custom_email_text=request.custom_email_text,
            deadline_days=request.deadline_days,
            estimated_cost=request.estimated_cost,
            next_phase_id=PhaseId.from_string(request.next_phase_id) if request.next_phase_id else None,  # Phase 12
            kanban_display=KanbanDisplayEnum(request.kanban_display) if request.kanban_display else None,
            style=style,
            validation_rules=request.validation_rules,
            recommended_rules=request.recommended_rules
        )

        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id_vo)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after update")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def delete_stage(self, stage_id: str) -> None:
        """Delete a stage."""
        command = DeleteStageCommand(id=WorkflowStageId.from_string(stage_id))
        self._command_bus.dispatch(command)

    def reorder_stages(self, workflow_id: str, request: ReorderStagesRequest) -> List[WorkflowStageResponse]:
        """Reorder stages in a workflow."""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        stage_ids_vo = [WorkflowStageId.from_string(sid) for sid in request.stage_ids_in_order]
        
        command = ReorderStagesCommand(
            workflow_id=workflow_id_vo,
            stage_ids_in_order=stage_ids_vo
        )

        self._command_bus.dispatch(command)

        query = ListStagesByWorkflowQuery(workflow_id=workflow_id_vo)
        dtos: List[WorkflowStageDto] = self._query_bus.query(query)

        return [WorkflowStageResponseMapper.dto_to_response(dto) for dto in dtos]

    def activate_stage(self, stage_id: str) -> WorkflowStageResponse:
        """Activate a stage."""
        stage_id_vo = WorkflowStageId.from_string(stage_id)
        command = ActivateStageCommand(id=stage_id_vo)
        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id_vo)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after activation")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def deactivate_stage(self, stage_id: str) -> WorkflowStageResponse:
        """Deactivate a stage."""
        stage_id_vo = WorkflowStageId.from_string(stage_id)
        command = DeactivateStageCommand(id=stage_id_vo)
        self._command_bus.dispatch(command)

        query = GetStageByIdQuery(id=stage_id_vo)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Stage not found after deactivation")

        return WorkflowStageResponseMapper.dto_to_response(dto)

    def update_stage_style(self, stage_id: str, style_request: UpdateStageStyleRequest) -> WorkflowStageResponse:
        """Update the visual style of a workflow stage."""
        stage_id_vo = WorkflowStageId.from_string(stage_id)
        
        # First get the current stage
        query = GetStageByIdQuery(id=stage_id_vo)
        dto: Optional[WorkflowStageDto] = self._query_bus.query(query)
        
        if not dto:
            raise Exception("Stage not found")

        # Create update command with style changes
        updated_style_dict = {
            **dto.style,
            **{k: v for k, v in style_request.model_dump().items() if v is not None}
        }
        
        updated_style = WorkflowStageStyle(
            background_color=updated_style_dict.get("background_color", "#ffffff"),
            text_color=updated_style_dict.get("text_color", "#000000"),
            icon=updated_style_dict.get("icon", "")
        )

        command = UpdateStageCommand(
            id=stage_id_vo,
            name=dto.name,
            description=dto.description,
            stage_type=WorkflowStageTypeEnum(dto.stage_type),
            allow_skip=dto.allow_skip,
            estimated_duration_days=dto.estimated_duration_days,
            default_role_ids=dto.default_role_ids,
            default_assigned_users=dto.default_assigned_users,
            email_template_id=dto.email_template_id,
            custom_email_text=dto.custom_email_text,
            deadline_days=dto.deadline_days,
            estimated_cost=dto.estimated_cost,
            next_phase_id=PhaseId.from_string(dto.next_phase_id) if dto.next_phase_id else None,
            kanban_display=KanbanDisplayEnum(dto.kanban_display),
            style=updated_style,
            validation_rules=dto.validation_rules,
            recommended_rules=dto.recommended_rules
        )
        self._command_bus.dispatch(command)

        # Return updated stage
        updated_query = GetStageByIdQuery(id=stage_id_vo)
        updated_dto: Optional[WorkflowStageDto] = self._query_bus.query(updated_query)

        if not updated_dto:
            raise Exception("Stage not found after style update")

        return WorkflowStageResponseMapper.dto_to_response(updated_dto)
