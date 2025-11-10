from dataclasses import dataclass

from src.customization.domain.entities.entity_customization import EntityCustomization
from src.customization.domain.exceptions import CustomFieldNotFound
from src.customization.domain.interfaces.entity_customization_repository_interface import EntityCustomizationRepositoryInterface
from src.customization.domain.value_objects.entity_customization_id import EntityCustomizationId
from src.customization.application.dtos.entity_customization_dto import EntityCustomizationDto
from src.customization.application.mappers.entity_customization_mapper import EntityCustomizationMapper
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetEntityCustomizationByIdQuery(Query):
    """Query to get an entity customization by ID"""
    id: EntityCustomizationId


class GetEntityCustomizationByIdQueryHandler(QueryHandler[GetEntityCustomizationByIdQuery, EntityCustomizationDto]):
    """Handler for getting an entity customization by ID"""

    def __init__(self, repository: EntityCustomizationRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetEntityCustomizationByIdQuery) -> EntityCustomizationDto:
        """Handle the get entity customization by ID query"""
        entity_customization = self._repository.get_by_id(query.id)
        
        if not entity_customization:
            raise CustomFieldNotFound(f"Entity customization with ID {query.id} not found")
        
        return EntityCustomizationMapper.entity_to_dto(entity_customization)

