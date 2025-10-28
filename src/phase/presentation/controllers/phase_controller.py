"""Phase controller for handling HTTP requests"""
from typing import List

from src.company.domain.value_objects.company_id import CompanyId
from src.phase.application.commands.create_phase_command import CreatePhaseCommand, CreatePhaseCommandHandler
from src.phase.application.commands.delete_phase_command import DeletePhaseCommand, DeletePhaseCommandHandler
from src.phase.application.commands.update_phase_command import UpdatePhaseCommand, UpdatePhaseCommandHandler
from src.phase.application.commands.archive_phase_command import ArchivePhaseCommand, ArchivePhaseCommandHandler
from src.phase.application.commands.activate_phase_command import ActivatePhaseCommand, ActivatePhaseCommandHandler
from src.phase.application.commands.initialize_company_phases_command import (
    InitializeCompanyPhasesCommand,
    InitializeCompanyPhasesCommandHandler
)
from src.phase.application.queries.get_phase_by_id_query import GetPhaseByIdQuery, GetPhaseByIdQueryHandler
from src.phase.application.queries.list_phases_by_company_query import (
    ListPhasesByCompanyQuery,
    ListPhasesByCompanyQueryHandler
)
from src.phase.domain.value_objects.phase_id import PhaseId
from src.phase.presentation.mappers.phase_mapper import PhaseMapper
from src.phase.presentation.schemas.phase_schemas import (
    CreatePhaseRequest,
    UpdatePhaseRequest,
    PhaseResponse
)


class PhaseController:
    """Controller for Phase operations"""

    def __init__(
        self,
        create_handler: CreatePhaseCommandHandler,
        update_handler: UpdatePhaseCommandHandler,
        delete_handler: DeletePhaseCommandHandler,
        archive_handler: ArchivePhaseCommandHandler,
        activate_handler: ActivatePhaseCommandHandler,
        get_by_id_handler: GetPhaseByIdQueryHandler,
        list_by_company_handler: ListPhasesByCompanyQueryHandler,
        initialize_handler: InitializeCompanyPhasesCommandHandler
    ):
        self.create_handler = create_handler
        self.update_handler = update_handler
        self.delete_handler = delete_handler
        self.archive_handler = archive_handler
        self.activate_handler = activate_handler
        self.get_by_id_handler = get_by_id_handler
        self.list_by_company_handler = list_by_company_handler
        self.initialize_handler = initialize_handler

    def create_phase(self, company_id: str, request: CreatePhaseRequest) -> PhaseResponse:
        """Create a new phase

        Args:
            company_id: Company ID
            request: Create phase request

        Returns:
            Created phase response
        """
        # Execute command
        command = CreatePhaseCommand(
            company_id=CompanyId.from_string(company_id),
            name=request.name,
            sort_order=request.sort_order,
            default_view=request.default_view,
            objective=request.objective
        )
        self.create_handler.execute(command)

        # Query the created phase (we need to return it)
        # Note: In a real implementation, we should return the ID from the command
        # For now, we'll list all phases and return the one that matches
        query = ListPhasesByCompanyQuery(company_id=CompanyId.from_string(company_id))
        phases = self.list_by_company_handler.handle(query)

        # Find the newly created phase by name and sort_order
        created_phase = next(
            (p for p in phases if p.name == request.name and p.sort_order == request.sort_order),
            phases[-1] if phases else None
        )

        if not created_phase:
            raise ValueError("Failed to create phase")

        return PhaseMapper.dto_to_response(created_phase)

    def update_phase(self, phase_id: str, request: UpdatePhaseRequest) -> PhaseResponse:
        """Update an existing phase

        Args:
            phase_id: Phase ID
            request: Update phase request

        Returns:
            Updated phase response
        """
        # Execute command
        command = UpdatePhaseCommand(
            phase_id=PhaseId.from_string(phase_id),
            name=request.name,
            sort_order=request.sort_order,
            default_view=request.default_view,
            objective=request.objective
        )
        self.update_handler.execute(command)

        # Query the updated phase
        query = GetPhaseByIdQuery(phase_id=PhaseId.from_string(phase_id))
        phase_dto = self.get_by_id_handler.handle(query)

        if not phase_dto:
            raise ValueError(f"Phase {phase_id} not found")

        return PhaseMapper.dto_to_response(phase_dto)

    def delete_phase(self, phase_id: str) -> None:
        """Delete a phase

        Args:
            phase_id: Phase ID to delete
        """
        command = DeletePhaseCommand(phase_id=PhaseId.from_string(phase_id))
        self.delete_handler.execute(command)

    def get_phase_by_id(self, phase_id: str) -> PhaseResponse:
        """Get a phase by ID

        Args:
            phase_id: Phase ID

        Returns:
            Phase response

        Raises:
            ValueError: If phase not found
        """
        query = GetPhaseByIdQuery(phase_id=PhaseId.from_string(phase_id))
        phase_dto = self.get_by_id_handler.handle(query)

        if not phase_dto:
            raise ValueError(f"Phase {phase_id} not found")

        return PhaseMapper.dto_to_response(phase_dto)

    def list_phases_by_company(self, company_id: str) -> List[PhaseResponse]:
        """List all phases for a company

        Args:
            company_id: Company ID

        Returns:
            List of phase responses
        """
        query = ListPhasesByCompanyQuery(company_id=CompanyId.from_string(company_id))
        phase_dtos = self.list_by_company_handler.handle(query)

        return [PhaseMapper.dto_to_response(dto) for dto in phase_dtos]

    def initialize_default_phases(self, company_id: str) -> List[PhaseResponse]:
        """Initialize default phases for a company (reset to defaults)

        This will create 4 default phases with their workflows:
        - Sourcing (Kanban) - Screening process
        - Evaluation (Kanban) - Interview and assessment
        - Offer and Pre-Onboarding (List) - Offer negotiation
        - Talent Pool (List) - Long-term tracking

        Args:
            company_id: Company ID

        Returns:
            List of created phase responses
        """
        # Execute initialization command
        command = InitializeCompanyPhasesCommand(
            company_id=CompanyId.from_string(company_id)
        )
        self.initialize_handler.execute(command)

        # Return the created phases
        return self.list_phases_by_company(company_id)

    def archive_phase(self, phase_id: str) -> PhaseResponse:
        """Archive a phase (soft delete)

        Args:
            phase_id: Phase ID to archive

        Returns:
            Archived phase response
        """
        # Execute archive command
        command = ArchivePhaseCommand(phase_id=phase_id)
        self.archive_handler.execute(command)

        # Query the archived phase
        query = GetPhaseByIdQuery(phase_id=PhaseId.from_string(phase_id))
        phase_dto = self.get_by_id_handler.handle(query)

        if not phase_dto:
            raise ValueError(f"Phase {phase_id} not found")

        return PhaseMapper.dto_to_response(phase_dto)

    def activate_phase(self, phase_id: str) -> PhaseResponse:
        """Activate a phase

        Args:
            phase_id: Phase ID to activate

        Returns:
            Activated phase response
        """
        # Execute activate command
        command = ActivatePhaseCommand(phase_id=phase_id)
        self.activate_handler.execute(command)

        # Query the activated phase
        query = GetPhaseByIdQuery(phase_id=PhaseId.from_string(phase_id))
        phase_dto = self.get_by_id_handler.handle(query)

        if not phase_dto:
            raise ValueError(f"Phase {phase_id} not found")

        return PhaseMapper.dto_to_response(phase_dto)
