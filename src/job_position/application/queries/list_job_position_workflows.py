from dataclasses import dataclass
from typing import List, Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.job_position.application.dtos.job_position_workflow_dto import JobPositionWorkflowDto
from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import JobPositionWorkflowRepositoryInterface


@dataclass
class ListJobPositionWorkflowsQuery(Query):
    """Query to list job position workflows for a company"""
    company_id: CompanyId


class ListJobPositionWorkflowsQueryHandler(QueryHandler[ListJobPositionWorkflowsQuery, List[JobPositionWorkflowDto]]):
    """Handler for listing job position workflows"""

    def __init__(self, workflow_repository: JobPositionWorkflowRepositoryInterface):
        self.workflow_repository = workflow_repository

    def handle(self, query: ListJobPositionWorkflowsQuery) -> List[JobPositionWorkflowDto]:
        """Handle the query - returns list of workflow DTOs"""
        workflows = self.workflow_repository.get_by_company_id(query.company_id)
        return [JobPositionWorkflowDto.from_entity(workflow) for workflow in workflows]

