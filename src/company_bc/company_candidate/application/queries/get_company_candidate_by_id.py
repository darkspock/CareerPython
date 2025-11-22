from dataclasses import dataclass
from typing import Optional

from src.company_bc.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_bc.company_candidate.application.mappers.company_candidate_mapper import CompanyCandidateMapper
from src.company_bc.company_candidate.domain.infrastructure.company_candidate_repository_interface import \
    CompanyCandidateRepositoryInterface
from src.company_bc.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface


@dataclass(frozen=True)
class GetCompanyCandidateByIdQuery(Query):
    """Query to get a company candidate by ID"""
    id: CompanyCandidateId


class GetCompanyCandidateByIdQueryHandler(QueryHandler[GetCompanyCandidateByIdQuery, Optional[CompanyCandidateDto]]):
    """Handler for getting a company candidate by ID"""

    def __init__(
        self,
        repository: CompanyCandidateRepositoryInterface,
        workflow_stage_repository: WorkflowStageRepositoryInterface
    ):
        self._repository = repository
        self._workflow_stage_repository = workflow_stage_repository

    def handle(self, query: GetCompanyCandidateByIdQuery) -> Optional[CompanyCandidateDto]:
        """Handle the get company candidate by ID query"""
        company_candidate = self._repository.get_by_id(query.id)

        if not company_candidate:
            return None

        # If candidate has a stage but no workflow, calculate workflow from stage
        if company_candidate.current_stage_id and not company_candidate.workflow_id:
            stage = self._workflow_stage_repository.get_by_id(company_candidate.current_stage_id)
            if stage:
                company_candidate.workflow_id = stage.workflow_id

        return CompanyCandidateMapper.entity_to_dto(company_candidate)
