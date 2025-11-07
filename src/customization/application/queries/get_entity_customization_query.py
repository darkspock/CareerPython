from dataclasses import dataclass
from typing import Optional

from src.customization.domain.entities.entity_customization import EntityCustomization
from src.customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from src.customization.application.dtos.entity_customization_dto import EntityCustomizationDto
from src.customization.application.mappers.entity_customization_mapper import EntityCustomizationMapper
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetEntityCustomizationQuery(Query):
    """Query to get an entity customization by entity type and entity ID"""
    entity_type: EntityCustomizationTypeEnum
    entity_id: str


class GetEntityCustomizationQueryHandler(QueryHandler[GetEntityCustomizationQuery, Optional[EntityCustomizationDto]]):
    """Handler for getting an entity customization"""

    def __init__(self, repository: EntityCustomizationRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetEntityCustomizationQuery) -> Optional[EntityCustomizationDto]:
        """Handle the get entity customization query
        
        Returns None if entity customization is not found (instead of raising an exception)
        """
        entity_customization = self._repository.get_by_entity(
            entity_type=query.entity_type,
            entity_id=query.entity_id
        )
        
        if not entity_customization:
            return None
        
        return EntityCustomizationMapper.entity_to_dto(entity_customization)

