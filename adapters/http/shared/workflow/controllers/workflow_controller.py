from typing import List, Optional, Any

from adapters.http.shared.workflow.mappers.workflow_mapper import WorkflowResponseMapper
from adapters.http.shared.workflow.mappers.workflow_stage_mapper import WorkflowStageResponseMapper
from adapters.http.shared.workflow.schemas.create_workflow_request import CreateWorkflowRequest
from adapters.http.shared.workflow.schemas.update_workflow_request import UpdateWorkflowRequest
from adapters.http.shared.workflow.schemas.workflow_response import WorkflowResponse
from src.company_bc.company.domain.value_objects import CompanyId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.application import CreateWorkflowCommand
from src.shared_bc.customization.workflow.application import DeactivateWorkflowCommand
from src.shared_bc.customization.workflow.application.commands.workflow.activate_workflow_command import \
    ActivateWorkflowCommand
from src.shared_bc.customization.workflow.application.commands.workflow.archive_workflow_command import \
    ArchiveWorkflowCommand
from src.shared_bc.customization.workflow.application.commands.workflow.delete_workflow_command import \
    DeleteWorkflowCommand
from src.shared_bc.customization.workflow.application.commands.workflow.set_as_default_workflow_command import \
    SetAsDefaultWorkflowCommand
from src.shared_bc.customization.workflow.application.commands.workflow.unset_as_default_workflow_command import \
    UnsetAsDefaultWorkflowCommand
from src.shared_bc.customization.workflow.application.commands.workflow.update_workflow_command import \
    UpdateWorkflowCommand
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
from src.shared_bc.customization.workflow.application.queries.stage.list_stages_by_workflow import \
    ListStagesByWorkflowQuery
from src.shared_bc.customization.workflow.application.queries.workflow.get_workflow_by_id import GetWorkflowByIdQuery
from src.shared_bc.customization.workflow.application.queries.workflow.list_workflows_by_company import \
    ListWorkflowsByCompanyQuery
from src.shared_bc.customization.workflow.application.queries.workflow.list_workflows_by_phase import \
    ListWorkflowsByPhaseQuery
from src.shared_bc.customization.workflow.application.services.workflow_response_service import WorkflowResponseService
from src.shared_bc.customization.workflow.domain.enums.workflow_display_enum import WorkflowDisplayEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_status_enum import WorkflowStatusEnum
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


class WorkflowController:
    """Controller for company workflow operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus, database: Any,
                 workflow_response_service: WorkflowResponseService):
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._database = database
        self._workflow_response_service = workflow_response_service

    def create_workflow(self, request: CreateWorkflowRequest) -> WorkflowResponse:
        """Create a new workflow"""

        workflow_id = WorkflowId.generate()

        command = CreateWorkflowCommand(
            id=workflow_id,
            company_id=CompanyId.from_string(request.company_id),
            workflow_type=WorkflowTypeEnum(request.workflow_type),
            name=request.name,
            description=request.description,
            display=WorkflowDisplayEnum(request.display),
            phase_id=PhaseId.from_string(request.phase_id) if request.phase_id else None,  # Phase 12
            is_default=request.is_default
        )

        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after creation")

        return WorkflowResponseMapper.dto_to_response(dto)

    def get_workflow_by_id(self, workflow_id: str) -> Optional[WorkflowResponse]:
        """Get a workflow by ID with enriched stages"""
        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            return None

        response = WorkflowResponseMapper.dto_to_response(dto)

        # Enrich with stages
        stages_query = ListStagesByWorkflowQuery(workflow_id=WorkflowId.from_string(dto.id))
        stage_dtos: List[WorkflowStageDto] = self._query_bus.query(stages_query)
        response.stages = [WorkflowStageResponseMapper.dto_to_response(stage_dto).model_dump() for stage_dto in
                           stage_dtos]

        return response

    def list_workflows_by_company(self, company_id: str, workflow_type: Optional[str] = None) -> List[WorkflowResponse]:
        """List all workflows for a company with enriched data"""

        company_id_vo = CompanyId.from_string(company_id)
        workflow_type_enum = WorkflowTypeEnum(workflow_type) if workflow_type else None

        query = ListWorkflowsByCompanyQuery(
            company_id=company_id_vo,
            workflow_type=workflow_type_enum
        )
        dtos: List[WorkflowDto] = self._query_bus.query(query)

        responses = []
        for dto in dtos:
            response = WorkflowResponseMapper.dto_to_response(dto)

            # Enrich with stages
            stages_query = ListStagesByWorkflowQuery(workflow_id=WorkflowId.from_string(dto.id))
            stage_dtos: List[WorkflowStageDto] = self._query_bus.query(stages_query)
            response.stages = [WorkflowStageResponseMapper.dto_to_response(stage_dto).model_dump() for stage_dto in
                               stage_dtos]

            responses.append(response)

        return responses

    def list_workflows_by_phase(self, phase_id: str, workflow_type: Optional[str] = None,
                                status: Optional[str] = None) -> List[WorkflowResponse]:
        """List workflows filtered by phase and optionally by workflow_type and status

        Args:
            phase_id: Phase ID to filter workflows
            workflow_type: Optional workflow type ('PO', 'CA', 'CO'). If None, returns all types.
            status: Optional status filter (active, draft, archived)

        Returns:
            List of workflow responses (simplified, without enrichment)
        """

        status_enum = WorkflowStatusEnum(status) if status else None
        workflow_type_enum = WorkflowTypeEnum(workflow_type) if workflow_type else None

        query = ListWorkflowsByPhaseQuery(
            phase_id=PhaseId.from_string(phase_id),
            workflow_type=workflow_type_enum,
            status=status_enum
        )
        dtos: List[WorkflowDto] = self._query_bus.query(query)

        return [WorkflowResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_workflow(self, workflow_id: str, request: UpdateWorkflowRequest) -> WorkflowResponse:
        """Update workflow information"""

        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = UpdateWorkflowCommand(
            id=workflow_id_vo,
            name=request.name,
            description=request.description,
            display=WorkflowDisplayEnum(request.display) if request.display else None,
            phase_id=PhaseId.from_string(request.phase_id) if request.phase_id else None  # Phase 12
        )

        self._command_bus.dispatch(command)

        # Use service to get enriched workflow response
        return self._workflow_response_service.get_enriched_workflow(workflow_id_vo)

    def activate_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Activate a workflow"""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = ActivateWorkflowCommand(id=workflow_id_vo)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id_vo)
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after activation")

        return WorkflowResponseMapper.dto_to_response(dto)

    def deactivate_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Deactivate a workflow"""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = DeactivateWorkflowCommand(workflow_id=workflow_id_vo)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id_vo)
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after deactivation")

        return WorkflowResponseMapper.dto_to_response(dto)

    def archive_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Archive a workflow"""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = ArchiveWorkflowCommand(workflow_id=workflow_id_vo)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id_vo)
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after archiving")

        return WorkflowResponseMapper.dto_to_response(dto)

    def set_as_default_workflow(self, workflow_id: str, company_id: str) -> WorkflowResponse:
        """Set a workflow as default for a company"""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = SetAsDefaultWorkflowCommand(
            workflow_id=workflow_id_vo,
            company_id=CompanyId.from_string(company_id)
        )
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id_vo)
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after setting as default")

        return WorkflowResponseMapper.dto_to_response(dto)

    def unset_as_default_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Unset a workflow as default"""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = UnsetAsDefaultWorkflowCommand(workflow_id=workflow_id_vo)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id_vo)

        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after unsetting as default")

        return WorkflowResponseMapper.dto_to_response(dto)

    def delete_workflow(self, workflow_id: str) -> None:
        """Delete a workflow permanently"""
        workflow_id_vo = WorkflowId.from_string(workflow_id)
        command = DeleteWorkflowCommand(workflow_id=workflow_id_vo)
        self._command_bus.dispatch(command)
