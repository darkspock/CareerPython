from dataclasses import dataclass
from typing import List

from src.customization.domain.interfaces.custom_field_repository_interface import CustomFieldRepositoryInterface
from src.customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.customization.application.dtos.custom_field_dto import CustomFieldDto
from src.customization.application.mappers.custom_field_mapper import CustomFieldMapper
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListCustomFieldsByEntityQuery(Query):
    """Query to list all custom fields for an entity customization"""
    entity_customization_id: EntityCustomizationId


class ListCustomFieldsByEntityQueryHandler(QueryHandler[ListCustomFieldsByEntityQuery, List[CustomFieldDto]]):
    """Handler for listing custom fields by entity customization"""

    def __init__(self, repository: CustomFieldRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListCustomFieldsByEntityQuery) -> List[CustomFieldDto]:
        """Handle the list custom fields query"""
        custom_fields = self._repository.list_by_entity_customization(query.entity_customization_id)
        return [CustomFieldMapper.entity_to_dto(field, str(query.entity_customization_id)) for field in custom_fields]

