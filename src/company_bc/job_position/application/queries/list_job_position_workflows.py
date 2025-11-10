from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.shared_bc.customization.workflow.application.dtos.workflow_dto import WorkflowDto
from src.shared_bc.customization.workflow.application.mappers.workflow_mapper import WorkflowMapper
from src.shared_bc.customization.workflow.domain.enums.workflow_type import WorkflowTypeEnum
from src.company_bc.company.domain.value_objects import CompanyId
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface


@dataclass
class ListJobPositionWorkflowsQuery(Query):
    """Query to list job position workflows for a company"""
    company_id: CompanyId


class ListJobPositionWorkflowsQueryHandler(QueryHandler[ListJobPositionWorkflowsQuery, List[WorkflowDto]]):
    """Handler for listing job position workflows"""

    def __init__(self, workflow_repository: WorkflowRepositoryInterface):
        self.workflow_repository = workflow_repository

    def handle(self, query: ListJobPositionWorkflowsQuery) -> List[WorkflowDto]:
        """Handle the query - returns list of workflow DTOs"""
        # Get workflows filtered by JOB_POSITION_OPENING type
        workflows = self.workflow_repository.list_by_company(
            company_id=query.company_id,
            workflow_type=WorkflowTypeEnum.JOB_POSITION_OPENING
        )
        return [WorkflowMapper.entity_to_dto(workflow) for workflow in workflows]
