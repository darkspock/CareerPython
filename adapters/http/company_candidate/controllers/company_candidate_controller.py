from datetime import date
from typing import List, Optional

from src.candidate_bc.candidate.application.commands import CreateCandidateCommand
from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.domain.value_objects import CandidateId
from src.company_bc.company.domain import CompanyId
from src.company_bc.company.domain.value_objects import CompanyUserId
from src.company_candidate.application.commands.archive_company_candidate_command import ArchiveCompanyCandidateCommand
from src.company_candidate.application.commands.assign_workflow_command import AssignWorkflowCommand
from src.company_candidate.application.commands.change_stage_command import ChangeStageCommand
from src.company_candidate.application.commands.confirm_company_candidate_command import ConfirmCompanyCandidateCommand
from src.company_candidate.application.commands.create_company_candidate_command import CreateCompanyCandidateCommand
from src.company_candidate.application.commands.reject_company_candidate_command import RejectCompanyCandidateCommand
from src.company_candidate.application.commands.transfer_ownership_command import TransferOwnershipCommand
from src.company_candidate.application.commands.update_company_candidate_command import UpdateCompanyCandidateCommand
from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.application.queries.get_company_candidate_by_company_and_candidate import \
    GetCompanyCandidateByCompanyAndCandidateQuery
from src.company_candidate.application.queries.get_company_candidate_by_id import GetCompanyCandidateByIdQuery
from src.company_candidate.application.queries.list_company_candidates_by_candidate import \
    ListCompanyCandidatesByCandidateQuery
from src.company_candidate.domain.enums import CandidatePriority
from src.company_candidate.domain.read_models.company_candidate_with_candidate_read_model import \
    CompanyCandidateWithCandidateReadModel
from src.company_candidate.domain.value_objects import CompanyCandidateId
from src.company_candidate.presentation.mappers.company_candidate_mapper import CompanyCandidateResponseMapper
from src.company_candidate.presentation.schemas.assign_workflow_request import AssignWorkflowRequest
from src.company_candidate.presentation.schemas.change_stage_request import ChangeStageRequest
from src.company_candidate.presentation.schemas.company_candidate_response import CompanyCandidateResponse
from src.company_candidate.presentation.schemas.create_company_candidate_request import CreateCompanyCandidateRequest
from src.company_candidate.presentation.schemas.update_company_candidate_request import UpdateCompanyCandidateRequest
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.auth_bc.user.domain.value_objects import UserId


class CompanyCandidateController:
    """Controller for company candidate operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_company_candidate(self, request: CreateCompanyCandidateRequest) -> CompanyCandidateResponse:
        """Create a new company candidate relationship"""

        # Determine candidate_id: either use existing or create new candidate
        if request.candidate_id:
            # Use existing candidate
            candidate_id_to_use = request.candidate_id
        else:
            # Create new candidate with minimal data
            if not request.candidate_name or not request.candidate_email:
                raise ValueError("candidate_name and candidate_email are required when creating new candidate")

            # Try to create a new candidate
            # If email already exists, we'll catch the exception and search for the existing candidate
            try:
                # Generate new candidate ID
                new_candidate_id = CandidateId.generate()

                # Use a special system user ID for company-created candidates without user accounts
                # This represents candidates that haven't registered yet
                system_user_id = UserId.from_string("01H0000000000000000000000")  # Special system user ID

                # Create candidate with minimal required data and placeholder values
                create_candidate_cmd = CreateCandidateCommand(
                    id=new_candidate_id,
                    name=request.candidate_name,
                    email=request.candidate_email,
                    phone=request.candidate_phone or "",
                    user_id=system_user_id,
                    date_of_birth=date(1900, 1, 1),  # Placeholder, can be updated later
                    city="Unknown",  # Placeholder, can be updated later
                    country="Unknown",  # Placeholder, can be updated later
                )
                self._command_bus.dispatch(create_candidate_cmd)
                candidate_id_to_use = str(new_candidate_id.value)

            except Exception as e:
                # If candidate creation fails due to duplicate email, search for existing candidate
                if "email ya está registrado" in str(e) or "already exists" in str(e).lower():
                    # Search for existing candidate by email using specific query
                    from src.candidate_bc.candidate.application.queries.get_candidate_by_email import GetCandidateByEmailQuery
                    search_query = GetCandidateByEmailQuery(email=request.candidate_email)
                    candidate_dto: Optional[CandidateDto] = self._query_bus.query(search_query)

                    if candidate_dto:
                        # Use the existing candidate
                        candidate_id_to_use = candidate_dto.id.value
                    else:
                        # Email error but candidate not found - re-raise original exception
                        raise e
                else:
                    # Different error - re-raise
                    raise e

        # Create company-candidate relationship
        company_candidate_id = CompanyCandidateId.generate()
        command = CreateCompanyCandidateCommand(
            id=company_candidate_id,
            company_id=CompanyId.from_string(request.company_id),
            candidate_id=CandidateId.from_string(candidate_id_to_use),
            created_by_user_id=CompanyUserId.from_string(request.created_by_user_id),
            position=request.position,
            source=request.source,
            department=request.department,
            priority=CandidatePriority(request.priority),
            visibility_settings=request.visibility_settings,
            tags=request.tags
        )

        self._command_bus.dispatch(command)

        # Query to get the created company candidate
        query = GetCompanyCandidateByIdQuery(id=company_candidate_id)
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def get_company_candidate_by_id(self, company_candidate_id: str) -> Optional[CompanyCandidateResponse]:
        """Get a company candidate by ID"""
        from src.company_candidate.application.queries.get_company_candidate_by_id_with_candidate_info import (
            GetCompanyCandidateByIdWithCandidateInfoQuery
        )

        query = GetCompanyCandidateByIdWithCandidateInfoQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        read_model: Optional[CompanyCandidateWithCandidateReadModel] = self._query_bus.query(query)

        if not read_model:
            return None

        # Get custom field values
        from typing import Dict, Any
        from src.customization.application.queries.get_custom_field_values_by_entity_query import GetCustomFieldValuesByEntityQuery
        from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
        
        custom_field_values_query = GetCustomFieldValuesByEntityQuery(
            entity_type=EntityCustomizationTypeEnum.CANDIDATE_APPLICATION,
            entity_id=company_candidate_id
        )
        custom_field_values: Dict[str, Any] = self._query_bus.query(custom_field_values_query) or {}

        # Use mapper to convert read model to response
        return CompanyCandidateResponseMapper.read_model_to_response(read_model, custom_field_values)

    def get_company_candidate_by_company_and_candidate(self, company_id: str, candidate_id: str) -> Optional[
        CompanyCandidateResponse]:
        """Get a company candidate by company ID and candidate ID"""
        query = GetCompanyCandidateByCompanyAndCandidateQuery(
            company_id=CompanyId.from_string(company_id),
            candidate_id=CandidateId.from_string(candidate_id)
        )
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def list_company_candidates_by_company(self, company_id: str) -> List[CompanyCandidateResponse]:
        """List all company candidates for a specific company with candidate info"""
        from src.company_candidate.application.queries.list_company_candidates_with_candidate_info import (
            ListCompanyCandidatesWithCandidateInfoQuery
        )

        # Use new query that returns read models with candidate info
        query = ListCompanyCandidatesWithCandidateInfoQuery(company_id=company_id)
        read_models: List[CompanyCandidateWithCandidateReadModel] = self._query_bus.query(query)

        # Use mapper to convert read models to responses
        return [
            CompanyCandidateResponseMapper.read_model_to_response(read_model)
            for read_model in read_models
        ]

    def list_company_candidates_by_candidate(self, candidate_id: str) -> List[CompanyCandidateResponse]:
        """List all company candidates for a specific candidate"""
        query = ListCompanyCandidatesByCandidateQuery(candidate_id=CandidateId.from_string(candidate_id))
        dtos: List[CompanyCandidateDto] = self._query_bus.query(query)

        return [CompanyCandidateResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_company_candidate(self, company_candidate_id: str,
                                 request: UpdateCompanyCandidateRequest) -> CompanyCandidateResponse:
        """Update company candidate information"""
        command = UpdateCompanyCandidateCommand(
            id=CompanyCandidateId.from_string(company_candidate_id),
            position=request.position,
            department=request.department,
            priority=CandidatePriority(request.priority) if request.priority else None,
            visibility_settings=request.visibility_settings,
            tags=request.tags
        )

        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def confirm_company_candidate(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Candidate confirms/accepts company invitation"""
        command = ConfirmCompanyCandidateCommand(id=CompanyCandidateId.from_string(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the confirmed company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def reject_company_candidate(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Candidate rejects/declines company invitation"""
        command = RejectCompanyCandidateCommand(id=CompanyCandidateId.from_string(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the rejected company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def archive_company_candidate(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Archive a company candidate relationship"""
        command = ArchiveCompanyCandidateCommand(id=CompanyCandidateId.from_string(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the archived company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def transfer_ownership(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Transfer ownership from company to user"""
        command = TransferOwnershipCommand(id=CompanyCandidateId.from_string(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def assign_workflow(self, company_candidate_id: str, request: AssignWorkflowRequest) -> CompanyCandidateResponse:
        """Assign a workflow to a company candidate"""
        command = AssignWorkflowCommand(
            id=CompanyCandidateId.from_string(company_candidate_id),
            workflow_id=WorkflowId.from_string(request.workflow_id),
            initial_stage_id=WorkflowStageId.from_string(request.initial_stage_id)
        )

        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def change_stage(self, company_candidate_id: str, request: ChangeStageRequest) -> CompanyCandidateResponse:
        """Change the workflow stage of a company candidate"""
        command = ChangeStageCommand(
            id=CompanyCandidateId.from_string(company_candidate_id),
            new_stage_id=WorkflowStageId.from_string(request.new_stage_id)
        )

        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId.from_string(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")

        return CompanyCandidateResponseMapper.dto_to_response(dto)

