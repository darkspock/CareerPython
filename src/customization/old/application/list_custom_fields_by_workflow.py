from dataclasses import dataclass
from typing import List

from src.customization.old.application.custom_field_dto import CustomFieldDto
from src.customization.old.application.custom_field_mapper import CustomFieldMapper
from src.workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListCustomFieldsByWorkflowQuery(Query):
    """Query to list all custom fields for a workflow"""
    workflow_id: str


class ListCustomFieldsByWorkflowQueryHandler(QueryHandler[ListCustomFieldsByWorkflowQuery, List[CustomFieldDto]]):
    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCustomFieldsByWorkflowQuery) -> List[CustomFieldDto]:
        workflow_id = WorkflowId.from_string(query.workflow_id)
        custom_fields = self._repository.list_by_workflow(workflow_id)
        return [CustomFieldMapper.entity_to_dto(field) for field in custom_fields]
