from typing import List, Optional

import ulid

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
from src.company_candidate.application.queries.list_company_candidates_by_company import \
    ListCompanyCandidatesByCompanyQuery
from src.company_candidate.domain.value_objects import CompanyCandidateId
from src.company_candidate.presentation.mappers.company_candidate_mapper import CompanyCandidateResponseMapper
from src.company_candidate.presentation.schemas.assign_workflow_request import AssignWorkflowRequest
from src.company_candidate.presentation.schemas.change_stage_request import ChangeStageRequest
from src.company_candidate.presentation.schemas.company_candidate_response import CompanyCandidateResponse
from src.company_candidate.presentation.schemas.create_company_candidate_request import CreateCompanyCandidateRequest
from src.company_candidate.presentation.schemas.update_company_candidate_request import UpdateCompanyCandidateRequest
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus


class CompanyCandidateController:
    """Controller for company candidate operations"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_company_candidate(self, request: CreateCompanyCandidateRequest) -> CompanyCandidateResponse:
        """Create a new company candidate relationship"""
        company_candidate_id = str(ulid.new())

        command = CreateCompanyCandidateCommand(
            id=company_candidate_id,
            company_id=request.company_id,
            candidate_id=request.candidate_id,
            created_by_user_id=request.created_by_user_id,
            position=request.position,
            department=request.department,
            priority=request.priority,
            visibility_settings=request.visibility_settings,
            tags=request.tags,
            internal_notes=request.internal_notes
        )

        self._command_bus.dispatch(command)

        # Query to get the created company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def get_company_candidate_by_id(self, company_candidate_id: str) -> Optional[CompanyCandidateResponse]:
        """Get a company candidate by ID"""
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def get_company_candidate_by_company_and_candidate(self, company_id: str, candidate_id: str) -> Optional[
        CompanyCandidateResponse]:
        """Get a company candidate by company ID and candidate ID"""
        query = GetCompanyCandidateByCompanyAndCandidateQuery(
            company_id=company_id,
            candidate_id=candidate_id
        )
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)

        if not dto:
            return None

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def list_company_candidates_by_company(self, company_id: str) -> List[CompanyCandidateResponse]:
        """List all company candidates for a specific company"""
        query = ListCompanyCandidatesByCompanyQuery(company_id=company_id)
        dtos: List[CompanyCandidateDto] = self._query_bus.query(query)

        return [CompanyCandidateResponseMapper.dto_to_response(dto) for dto in dtos]

    def list_company_candidates_by_candidate(self, candidate_id: str) -> List[CompanyCandidateResponse]:
        """List all company candidates for a specific candidate"""
        query = ListCompanyCandidatesByCandidateQuery(candidate_id=candidate_id)
        dtos: List[CompanyCandidateDto] = self._query_bus.query(query)

        return [CompanyCandidateResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_company_candidate(self, company_candidate_id: str,
                                 request: UpdateCompanyCandidateRequest) -> CompanyCandidateResponse:
        """Update company candidate information"""
        command = UpdateCompanyCandidateCommand(
            id=company_candidate_id,
            position=request.position,
            department=request.department,
            priority=request.priority,
            visibility_settings=request.visibility_settings,
            tags=request.tags,
            internal_notes=request.internal_notes
        )

        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def confirm_company_candidate(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Candidate confirms/accepts company invitation"""
        command = ConfirmCompanyCandidateCommand(id=CompanyCandidateId(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the confirmed company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def reject_company_candidate(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Candidate rejects/declines company invitation"""
        command = RejectCompanyCandidateCommand(id=CompanyCandidateId(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the rejected company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def archive_company_candidate(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Archive a company candidate relationship"""
        command = ArchiveCompanyCandidateCommand(id=CompanyCandidateId(company_candidate_id))
        self._command_bus.dispatch(command)

        # Query to get the archived company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def transfer_ownership(self, company_candidate_id: str) -> CompanyCandidateResponse:
        """Transfer ownership from company to user"""
        command = TransferOwnershipCommand(id=company_candidate_id)
        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=CompanyCandidateId(company_candidate_id))
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")
        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def assign_workflow(self, company_candidate_id: str, request: AssignWorkflowRequest) -> CompanyCandidateResponse:
        """Assign a workflow to a company candidate"""
        command = AssignWorkflowCommand(
            id=company_candidate_id,
            workflow_id=request.workflow_id,
            initial_stage_id=request.initial_stage_id
        )

        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=company_candidate_id)
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")

        return CompanyCandidateResponseMapper.dto_to_response(dto)

    def change_stage(self, company_candidate_id: str, request: ChangeStageRequest) -> CompanyCandidateResponse:
        """Change the workflow stage of a company candidate"""
        command = ChangeStageCommand(
            id=company_candidate_id,
            new_stage_id=request.new_stage_id
        )

        self._command_bus.dispatch(command)

        # Query to get the updated company candidate
        query = GetCompanyCandidateByIdQuery(id=company_candidate_id)
        dto: Optional[CompanyCandidateDto] = self._query_bus.query(query)
        if not dto:
            raise Exception("Company candidate not found")

        return CompanyCandidateResponseMapper.dto_to_response(dto)
