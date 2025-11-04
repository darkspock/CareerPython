from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.job_position.application.dtos.job_position_workflow_dto import JobPositionWorkflowDto
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import JobPositionWorkflowRepositoryInterface


@dataclass
class GetJobPositionWorkflowQuery(Query):
    """Query to get a job position workflow by ID"""
    workflow_id: JobPositionWorkflowId


class GetJobPositionWorkflowQueryHandler(QueryHandler[GetJobPositionWorkflowQuery, JobPositionWorkflowDto]):
    """Handler for getting a job position workflow"""

    def __init__(self, workflow_repository: JobPositionWorkflowRepositoryInterface):
        self.workflow_repository = workflow_repository

    def handle(self, query: GetJobPositionWorkflowQuery) -> JobPositionWorkflowDto:
        """Handle the query - returns workflow DTO"""
        workflow = self.workflow_repository.get_by_id(query.workflow_id)
        if not workflow:
            raise ValueError(f"Workflow with id {query.workflow_id.value} not found")

        return JobPositionWorkflowDto.from_entity(workflow)

