import ulid
from typing import List, Optional

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
from src.company_workflow.presentation.schemas.create_workflow_request import CreateWorkflowRequest
from src.company_workflow.presentation.schemas.update_workflow_request import UpdateWorkflowRequest
from src.company_workflow.presentation.schemas.company_workflow_response import CompanyWorkflowResponse
from src.company_workflow.presentation.mappers.company_workflow_mapper import CompanyWorkflowResponseMapper


class CompanyWorkflowController:
    """Controller for company workflow operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_workflow(self, request: CreateWorkflowRequest) -> CompanyWorkflowResponse:
        """Create a new workflow"""
        workflow_id = str(ulid.new())

        command = CreateWorkflowCommand(
            id=workflow_id,
            company_id=request.company_id,
            name=request.name,
            description=request.description,
            is_default=request.is_default
        )

        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def get_workflow_by_id(self, workflow_id: str) -> Optional[CompanyWorkflowResponse]:
        """Get a workflow by ID"""
        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        if not dto:
            return None

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def list_workflows_by_company(self, company_id: str) -> List[CompanyWorkflowResponse]:
        """List all workflows for a company"""
        query = ListWorkflowsByCompanyQuery(company_id=company_id)
        dtos = self._query_bus.query(query)

        return [CompanyWorkflowResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_workflow(self, workflow_id: str, request: UpdateWorkflowRequest) -> CompanyWorkflowResponse:
        """Update workflow information"""
        command = UpdateWorkflowCommand(
            id=workflow_id,
            name=request.name,
            description=request.description
        )

        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def activate_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Activate a workflow"""
        command = ActivateWorkflowCommand(id=workflow_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def deactivate_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Deactivate a workflow"""
        command = DeactivateWorkflowCommand(workflow_id=workflow_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def archive_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Archive a workflow"""
        command = ArchiveWorkflowCommand(workflow_id=workflow_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def set_as_default_workflow(self, workflow_id: str, company_id: str) -> CompanyWorkflowResponse:
        """Set a workflow as default for a company"""
        command = SetAsDefaultWorkflowCommand(workflow_id=workflow_id, company_id=company_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)

    def unset_as_default_workflow(self, workflow_id: str) -> CompanyWorkflowResponse:
        """Unset a workflow as default"""
        command = UnsetAsDefaultWorkflowCommand(workflow_id=workflow_id)
        self._command_bus.dispatch(command)

        query = GetWorkflowByIdQuery(id=workflow_id)
        dto = self._query_bus.query(query)

        return CompanyWorkflowResponseMapper.dto_to_response(dto)
