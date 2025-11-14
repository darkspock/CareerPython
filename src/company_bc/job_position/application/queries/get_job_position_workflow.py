from dataclasses import dataclass
from typing import Optional

from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.mappers.workflow_mapper import WorkflowMapper
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId


@dataclass
class GetJobPositionWorkflowQuery(Query):
    """Query to get a job position workflow by ID"""
    workflow_id: JobPositionWorkflowId


class GetJobPositionWorkflowQueryHandler(QueryHandler[GetJobPositionWorkflowQuery, Optional[WorkflowDto]]):
    """Handler for getting a job position workflow"""

    def __init__(self, workflow_repository: WorkflowRepositoryInterface):
        self.workflow_repository = workflow_repository

    def handle(self, query: GetJobPositionWorkflowQuery) -> Optional[WorkflowDto]:
        """Handle the query - returns workflow DTO"""
        # Convert JobPositionWorkflowId to WorkflowId
        workflow_id = WorkflowId.from_string(query.workflow_id.value)
        workflow = self.workflow_repository.get_by_id(workflow_id)
        if not workflow:
            return None

        return WorkflowMapper.entity_to_dto(workflow)
