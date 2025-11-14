"""List stage assignments query"""
from dataclasses import dataclass
from typing import List

from src.company_bc.position_stage_assignment.application.queries.position_stage_assignment_dto import \
    PositionStageAssignmentDto
from src.company_bc.position_stage_assignment.domain import PositionStageAssignmentRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class ListStageAssignmentsQuery(Query):
    """Query to list stage assignments for a position"""
    position_id: str


class ListStageAssignmentsQueryHandler(QueryHandler[ListStageAssignmentsQuery, List[PositionStageAssignmentDto]]):
    """Handler for listing stage assignments"""

    def __init__(self, repository: PositionStageAssignmentRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListStageAssignmentsQuery) -> List[PositionStageAssignmentDto]:
        """Execute the query"""
        assignments = self.repository.list_by_position(query.position_id)
        return [PositionStageAssignmentDto.from_entity(a) for a in assignments]
