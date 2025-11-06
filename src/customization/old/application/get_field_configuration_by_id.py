from dataclasses import dataclass
from typing import Optional

from src.customization.old.application.field_configuration_dto import FieldConfigurationDto
from src.customization.old.application.field_configuration_mapper import FieldConfigurationMapper
from src.workflow.domain.infrastructure.field_configuration_repository_interface import FieldConfigurationRepositoryInterface
from src.workflow.domain.value_objects.field_configuration_id import FieldConfigurationId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetFieldConfigurationByIdQuery(Query):
    """Query to get a field configuration by ID"""
    id: str


class GetFieldConfigurationByIdQueryHandler(QueryHandler[GetFieldConfigurationByIdQuery, Optional[FieldConfigurationDto]]):
    def __init__(self, repository: FieldConfigurationRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetFieldConfigurationByIdQuery) -> Optional[FieldConfigurationDto]:
        field_configuration_id = FieldConfigurationId.from_string(query.id)
        field_configuration = self._repository.get_by_id(field_configuration_id)
        if not field_configuration:
            return None
        return FieldConfigurationMapper.entity_to_dto(field_configuration)
