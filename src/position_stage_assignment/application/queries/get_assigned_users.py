"""Get assigned users query"""
from dataclasses import dataclass
from typing import List

from src.position_stage_assignment.domain import PositionStageAssignmentRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetAssignedUsersQuery(Query):
    """Query to get assigned users for a position-stage combination"""
    position_id: str
    stage_id: str


class GetAssignedUsersQueryHandler(QueryHandler[GetAssignedUsersQuery, List[str]]):
    """Handler for getting assigned users"""

    def __init__(self, repository: PositionStageAssignmentRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetAssignedUsersQuery) -> List[str]:
        """Execute the query"""
        return self.repository.get_assigned_users(query.position_id, query.stage_id)
