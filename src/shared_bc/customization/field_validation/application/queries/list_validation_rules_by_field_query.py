from dataclasses import dataclass
from typing import List

from src.customization.domain.value_objects.custom_field_id import CustomFieldId
from src.framework.application.query_bus import Query
from src.framework.application.query_bus import QueryHandler
from src.shared_bc.customization.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface
from src.shared_bc.customization.field_validation.application.dtos.validation_rule_dto import ValidationRuleDto
from src.shared_bc.customization.field_validation.application.mappers.validation_rule_mapper import ValidationRuleMapper


@dataclass(frozen=True)
class ListValidationRulesByFieldQuery(Query):
    """Query to list validation rules by custom field."""

    custom_field_id: CustomFieldId
    active_only: bool = False


class ListValidationRulesByFieldQueryHandler(QueryHandler[ListValidationRulesByFieldQuery, List[ValidationRuleDto]]):
    """Handler for listing validation rules by custom field."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListValidationRulesByFieldQuery) -> List[ValidationRuleDto]:
        """Handle the query."""
        validation_rules = self.repository.list_by_custom_field(
            field_id=query.custom_field_id,
            active_only=query.active_only
        )

        return [ValidationRuleMapper.entity_to_dto(rule) for rule in validation_rules]
