import ulid
from typing import List, Optional, Any
from sqlalchemy import func

from src.company_workflow.application.dtos.company_workflow_dto import CompanyWorkflowDto
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.company_workflow.application.commands.create_workflow_command import CreateWorkflowCommand
from src.company_workflow.application.commands.update_workflow_command import UpdateWorkflowCommand
from src.company_workflow.application.commands.activate_workflow_command import ActivateWorkflowCommand
from src.company_workflow.application.commands.deactivate_workflow_command import DeactivateWorkflowCommand
from src.company_workflow.application.commands.archive_workflow_command import ArchiveWorkflowCommand
from src.company_workflow.application.commands.set_as_default_workflow_command import SetAsDefaultWorkflowCommand
from src.company_workflow.application.commands.unset_as_default_workflow_command import UnsetAsDefaultWorkflowCommand
from src.company_workflow.application.queries.get_workflow_by_id import GetWorkflowByIdQuery
from src.company_workflow.application.queries.list_workflows_by_company import ListWorkflowsByCompanyQuery
from src.company_workflow.application.queries.list_workflows_by_phase import ListWorkflowsByPhaseQuery
from src.company_workflow.application.queries.list_stages_by_workflow import ListStagesByWorkflowQuery
from src.company_workflow.presentation.schemas.create_workflow_request import CreateWorkflowRequest
from src.company_workflow.presentation.schemas.update_workflow_request import UpdateWorkflowRequest
from src.company_workflow.presentation.schemas.company_workflow_response import CompanyWorkflowResponse
from src.company_workflow.presentation.mappers.company_workflow_mapper import CompanyWorkflowResponseMapper
from src.company_workflow.presentation.mappers.workflow_stage_mapper import WorkflowStageResponseMapper
from src.company_candidate.infrastructure.models.company_candidate_model import CompanyCandidateModel
from src.job_position.infrastructure.models.job_position_model import JobPositionModel
from src.candidate_application.infrastructure.models.candidate_application_model import CandidateApplicationModel


class CompanyWorkflowController:
    """Controller for company workflow operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus, database: Any):
        self._command_bus = command_bus
        self._query_bus = query_bus
        self._database = database

    def create_workflow(self, request: CreateWorkflowRequest) -> CompanyWorkflowResponse:
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

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after creation")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def get_workflow_by_id(self, workflow_id: str) -> Optional[CompanyWorkflowResponse]:
        """Get a workflow by ID"""
        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def list_workflows_by_company(self, company_id: str) -> List[CompanyWorkflowResponse]:
        """List all workflows for a company with enriched data"""
        query = ListWorkflowsByCompanyQuery(company_id=company_id)
        dtos: List[CompanyWorkflowDto] = self._query_bus.query(query)

        responses = []
        for dto in dtos:
            response = CompanyWorkflowResponseMapper.dto_to_response(dto)

            # Enrich with stages
            from src.company_workflow.application.dtos.workflow_stage_dto import WorkflowStageDto
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
                from src.job_position.domain.enums.job_position_status import JobPositionStatusEnum
                active_position_count = session.query(func.count(func.distinct(CandidateApplicationModel.job_position_id))).join(
                    CompanyCandidateModel,
                    CompanyCandidateModel.candidate_id == CandidateApplicationModel.candidate_id
                ).join(
                    JobPositionModel,
                    JobPositionModel.id == CandidateApplicationModel.job_position_id
                ).filter(
                    CompanyCandidateModel.workflow_id == dto.id,
                    JobPositionModel.status == JobPositionStatusEnum.OPEN,
                    JobPositionModel.company_id == company_id
                ).scalar() or 0

                response.active_candidate_count = active_candidate_count
                response.active_position_count = active_position_count
                response.candidate_count = active_candidate_count  # For backward compatibility

            responses.append(response)

        return responses

    def list_workflows_by_phase(self, phase_id: str, status: Optional[str] = None) -> List[CompanyWorkflowResponse]:
        """List workflows filtered by phase and optionally by status

        Args:
            phase_id: Phase ID to filter workflows
            status: Optional status filter (active, draft, archived)

        Returns:
            List of workflow responses (simplified, without enrichment)
        """
        query = ListWorkflowsByPhaseQuery(phase_id=phase_id, status=status)
        dtos: List[CompanyWorkflowDto] = self._query_bus.query(query)

        return [CompanyWorkflowResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_workflow(self, workflow_id: str, request: UpdateWorkflowRequest) -> CompanyWorkflowResponse:
        """Update workflow information"""
        command = UpdateWorkflowCommand(
            id=workflow_id,
            name=request.name,
            description=request.description,
            phase_id=request.phase_id  # Phase 12
        )

        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after update")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def activate_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Activate a workflow"""
        command = ActivateWorkflowCommand(id=workflow_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after activation")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def deactivate_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Deactivate a workflow"""
        command = DeactivateWorkflowCommand(workflow_id=CompanyWorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after deactivation")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def archive_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Archive a workflow"""
        command = ArchiveWorkflowCommand(workflow_id=CompanyWorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after archiving")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def set_as_default_workflow(self, workflow_id: str, company_id: str) -> CompanyWorkflowResponse:
        """Set a workflow as default for a company"""
        command = SetAsDefaultWorkflowCommand(
            workflow_id=CompanyWorkflowId.from_string(workflow_id),
            company_id=CompanyId.from_string(company_id)
        )
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))
        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after setting as default")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def unset_as_default_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Unset a workflow as default"""
        command = UnsetAsDefaultWorkflowCommand(workflow_id=CompanyWorkflowId.from_string(workflow_id))
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=CompanyWorkflowId.from_string(workflow_id))

        dto: Optional[CompanyWorkflowDto] = self._query_bus.query(query)

        if not dto:
            raise Exception("Workflow not found after unsetting as default")

        return CompanyWorkflowResponseMapper.dto_to_response(dto)
