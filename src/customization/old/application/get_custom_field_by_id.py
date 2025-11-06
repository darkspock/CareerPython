from dataclasses import dataclass
from typing import Optional

from src.customization.old.application.custom_field_dto import CustomFieldDto
from src.customization.old.application.custom_field_mapper import CustomFieldMapper
from src.workflow.domain.infrastructure.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.workflow.domain.value_objects.custom_field_id import CustomFieldId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetCustomFieldByIdQuery(Query):
    """Query to get a custom field by ID"""
    id: str


class GetCustomFieldByIdQueryHandler(QueryHandler[GetCustomFieldByIdQuery, Optional[CustomFieldDto]]):
    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetCustomFieldByIdQuery) -> Optional[CustomFieldDto]:
        custom_field_id = CustomFieldId.from_string(query.id)
        custom_field = self._repository.get_by_id(custom_field_id)
        if not custom_field:
            return None
        return CustomFieldMapper.entity_to_dto(custom_field)
