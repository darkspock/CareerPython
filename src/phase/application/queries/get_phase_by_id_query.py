"""Get phase by ID query"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.phase.domain.entities.phase import Phase
from src.phase.domain.enums.default_view_enum import DefaultView
from src.phase.domain.enums.phase_status_enum import PhaseStatus
from src.phase.domain.infrastructure.phase_repository_interface import PhaseRepositoryInterface
from src.phase.domain.value_objects.phase_id import PhaseId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class PhaseDto:
    """Phase data transfer object"""
    id: str
    company_id: str
    workflow_type: str  # WorkflowTypeEnum value as string
    name: str
    sort_order: int
    default_view: DefaultView
    status: PhaseStatus
    objective: Optional[str]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(phase: Phase) -> "PhaseDto":
        """Create DTO from Phase entity"""
        return PhaseDto(
            id=phase.id.value,
            company_id=phase.company_id.value,
            workflow_type=phase.workflow_type.value,
            name=phase.name,
            sort_order=phase.sort_order,
            default_view=phase.default_view,
            status=phase.status,
            objective=phase.objective,
            created_at=phase.created_at,
            updated_at=phase.updated_at
        )


@dataclass
class GetPhaseByIdQuery(Query):
    """Query to get a phase by ID"""
    phase_id: PhaseId


class GetPhaseByIdQueryHandler(QueryHandler[GetPhaseByIdQuery, Optional[PhaseDto]]):
    """Handler for GetPhaseByIdQuery"""

    def __init__(self, phase_repository: PhaseRepositoryInterface):
        self.phase_repository = phase_repository

    def handle(self, query: GetPhaseByIdQuery) -> Optional[PhaseDto]:
        """Handle the query to get a phase by ID"""
        phase = self.phase_repository.get_by_id(query.phase_id)

        if not phase:
            return None

        return PhaseDto.from_entity(phase)
