from dataclasses import dataclass
from typing import Optional

from src.shared.application.query_bus import Query, QueryHandler
from src.customization.old.application.custom_field_value_dto import CustomFieldValueDto
from src.customization.old.application.custom_field_value_mapper import CustomFieldValueMapper
from src.workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
from src.workflow.domain.infrastructure.custom_field_value_repository_interface import CustomFieldValueRepositoryInterface


@dataclass(frozen=True)
class GetCustomFieldValueByIdQuery(Query):
    """Query to get a custom field value by ID"""
    id: str


class GetCustomFieldValueByIdQueryHandler(QueryHandler[GetCustomFieldValueByIdQuery, Optional[CustomFieldValueDto]]):
    """Handler for getting custom field value by ID"""

    def __init__(self, repository: CustomFieldValueRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCustomFieldValueByIdQuery) -> Optional[CustomFieldValueDto]:
        """Handle the get custom field value by ID query"""
        custom_field_value = self._repository.get_by_id(CustomFieldValueId(query.id))
        if not custom_field_value:
            return None
        
        return CustomFieldValueMapper.entity_to_dto(custom_field_value)
