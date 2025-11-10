from dataclasses import dataclass
from typing import Dict, Any, Optional

from src.customization.domain.enums.entity_customization_type_enum import EntityCustomizationTypeEnum
from src.framework.application.query_bus import Query, QueryHandler
from core.database import SQLAlchemyDatabase
from src.customization.infrastructure.models.custom_field_value_model import CustomFieldValueModel


@dataclass(frozen=True)
class GetCustomFieldValuesByEntityQuery(Query):
    """Query to get custom field values for an entity"""
    entity_type: EntityCustomizationTypeEnum
    entity_id: str


class GetCustomFieldValuesByEntityQueryHandler(QueryHandler[GetCustomFieldValuesByEntityQuery, Dict[str, Any]]):
    """Handler for getting custom field values by entity"""

    def __init__(self, database: SQLAlchemyDatabase):
        self._database = database

    def handle(self, query: GetCustomFieldValuesByEntityQuery) -> Dict[str, Any]:
        """Handle the get custom field values query"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldValueModel).filter_by(
                entity_type=query.entity_type.value,
                entity_id=query.entity_id
            ).first()
            
            if model and model.values:
                return model.values
            return {}

