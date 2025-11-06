import ulid
from typing import List, Optional, Any
from sqlalchemy import func

from src.workflow.application.dtos.candidate_application_workflow_dto import WorkflowDto
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.workflow.application.commands.workflow.create_workflow_command import CreateWorkflowCommand
from src.workflow.application.commands.workflow.update_workflow_command import UpdateWorkflowCommand
from src.workflow.application.commands.workflow.activate_workflow_command import ActivateWorkflowCommand
from src.workflow.application.commands.workflow.deactivate_workflow_command import DeactivateWorkflowCommand
from src.workflow.application.commands.workflow.archive_workflow_command import ArchiveWorkflowCommand
from src.workflow.application.commands.workflow.delete_workflow_command import DeleteWorkflowCommand
from src.workflow.application.commands.workflow.set_as_default_workflow_command import SetAsDefaultWorkflowCommand
from src.workflow.application.commands.workflow.unset_as_default_workflow_command import UnsetAsDefaultWorkflowCommand
from src.workflow.application.queries.workflow.get_workflow_by_id import GetWorkflowByIdQuery
from src.workflow.application.queries.workflow.list_workflows_by_company import ListWorkflowsByCompanyQuery
from src.workflow.application.queries.workflow.list_workflows_by_phase import ListWorkflowsByPhaseQuery
from src.workflow.application.queries.stage.list_stages_by_workflow import ListStagesByWorkflowQuery
from src.workflow.presentation.schemas.create_workflow_request import CreateWorkflowRequest
from src.workflow.presentation.schemas.update_workflow_request import UpdateWorkflowRequest
from src.workflow.presentation.schemas.candidate_application_workflow_response import WorkflowResponse
from src.workflow.presentation.mappers.candidate_application_workflow_mapper import WorkflowResponseMapper
from src.workflow.presentation.mappers.workflow_stage_mapper import WorkflowStageResponseMapper
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel


class WorkflowController:
    """Controller for company workflow operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus, database: Any):
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._database = database

    def create_workflow(self, request: CreateWorkflowRequest) -> WorkflowResponse:
        """Create a new workflow"""
        workflow_id = str(ulid.new())

        command = CreateWorkflowCommand(
            id=workflow_id,
            company_id=request.company_id,
            name=request.name,
            description=request.description,
            phase_id=request.phase_id,  # Phase 12
            is_default=request.is_default
        )

        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after creation")

        return WorkflowResponseMapper.dto_to_response(dto)

    def get_workflow_by_id(self, workflow_id: str) -> Optional[WorkflowResponse]:
        """Get a workflow by ID"""
        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            return None

        return WorkflowResponseMapper.dto_to_response(dto)

    def list_workflows_by_company(self, company_id: str) -> List[WorkflowResponse]:
        """List all workflows for a company with enriched data"""
        query = ListWorkflowsByCompanyQuery(company_id=company_id)
        dtos: List[WorkflowDto] = self._query_bus.query(query)

        responses = []
        for dto in dtos:
            response = WorkflowResponseMapper.dto_to_response(dto)

            # Enrich with stages
            from src.workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
            stages_query = ListStagesByWorkflowQuery(workflow_id=dto.id)
            stage_dtos: List[WorkflowStageDto] = self._query_bus.query(stages_query)
            response.stages = [WorkflowStageResponseMapper.dto_to_response(stage_dto).dict() for stage_dto in stage_dtos]

            # Enrich with counts using database queries
            with self._database.get_session() as session:
                # Count active candidates in this workflow
                from src.company_candidate.domain.enums.company_candidate_status import CompanyCandidateStatus
                active_candidate_count = session.query(func.count(CompanyCandidateModel.id)).filter(
                    CompanyCandidateModel.workflow_id == dto.id,
                    CompanyCandidateModel.status == CompanyCandidateStatus.ACTIVE.value
                ).scalar() or 0

                # Count distinct open positions that have candidates in this workflow
                # through candidate_applications
                from src.job_position.domain.enums.job_position_visibility import JobPositionVisibilityEnum
                active_position_count = session.query(func.count(func.distinct(CandidateApplicationModel.job_position_id))).join(
                    CompanyCandidateModel,
                    CompanyCandidateModel.candidate_id == CandidateApplicationModel.candidate_id
                ).join(
                    JobPositionModel,
                    JobPositionModel.id == CandidateApplicationModel.job_position_id
                ).filter(
                    CompanyCandidateModel.workflow_id == dto.id,
                    JobPositionModel.visibility == JobPositionVisibilityEnum.PUBLIC,  # TODO: Check status from workflow stage
                    JobPositionModel.company_id == company_id
                ).scalar() or 0

                response.active_candidate_count = active_candidate_count
                response.active_position_count = active_position_count
                response.candidate_count = active_candidate_count  # For backward compatibility

            responses.append(response)

        return responses

    def list_workflows_by_phase(self, phase_id: str, status: Optional[str] = None) -> List[WorkflowResponse]:
        """List workflows filtered by phase and optionally by status

        Args:
            phase_id: Phase ID to filter workflows
            status: Optional status filter (active, draft, archived)

        Returns:
            List of workflow responses (simplified, without enrichment)
        """
        query = ListWorkflowsByPhaseQuery(phase_id=phase_id, status=status)
        dtos: List[WorkflowDto] = self._query_bus.query(query)

        return [WorkflowResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_workflow(self, workflow_id: str, request: UpdateWorkflowRequest) -> WorkflowResponse:
        """Update workflow information"""
        command = UpdateWorkflowCommand(
            id=workflow_id,
            name=request.name,
            description=request.description,
            phase_id=request.phase_id  # Phase 12
        )

        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after update")

        return WorkflowResponseMapper.dto_to_response(dto)

    def activate_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Activate a workflow"""
        command = ActivateWorkflowCommand(id=workflow_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after activation")

        return WorkflowResponseMapper.dto_to_response(dto)

    def deactivate_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Deactivate a workflow"""
        command = DeactivateWorkflowCommand(workflow_id=WorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after deactivation")

        return WorkflowResponseMapper.dto_to_response(dto)

    def archive_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Archive a workflow"""
        command = ArchiveWorkflowCommand(workflow_id=WorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after archiving")

        return WorkflowResponseMapper.dto_to_response(dto)

    def set_as_default_workflow(self, workflow_id: str, company_id: str) -> WorkflowResponse:
        """Set a workflow as default for a company"""
        command = SetAsDefaultWorkflowCommand(
            workflow_id=WorkflowId.from_string(workflow_id),
            company_id=CompanyId.from_string(company_id)
        )
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))
        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after setting as default")

        return WorkflowResponseMapper.dto_to_response(dto)

    def unset_as_default_workflow(self, workflow_id: str) -> WorkflowResponse:
        """Unset a workflow as default"""
        command = UnsetAsDefaultWorkflowCommand(workflow_id=WorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=WorkflowId.from_string(workflow_id))

        dto: Optional[WorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after unsetting as default")

        return WorkflowResponseMapper.dto_to_response(dto)

    def delete_workflow(self, workflow_id: str) -> None:
        """Delete a workflow permanently"""
        command = DeleteWorkflowCommand(workflow_id=WorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)
