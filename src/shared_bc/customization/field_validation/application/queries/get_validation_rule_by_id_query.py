from dataclasses import dataclass
from typing import Optional

from src.framework.application.query_bus import Query
from src.framework.application.query_bus import QueryHandler
from src.shared_bc.customization.field_validation.application.dtos.validation_rule_dto import ValidationRuleDto
from src.shared_bc.customization.field_validation.application.mappers.validation_rule_mapper import ValidationRuleMapper
from src.shared_bc.customization.field_validation.domain.infrastructure.validation_rule_repository_interface import \
    ValidationRuleRepositoryInterface
from src.shared_bc.customization.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId


@dataclass(frozen=True)
class GetValidationRuleByIdQuery(Query):
    """Query to get a validation rule by ID."""

    id: ValidationRuleId


class GetValidationRuleByIdQueryHandler(QueryHandler[GetValidationRuleByIdQuery, Optional[ValidationRuleDto]]):
    """Handler for getting a validation rule by ID."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def handle(self, query: GetValidationRuleByIdQuery) -> Optional[ValidationRuleDto]:
        """Handle the query."""
        validation_rule = self.repository.get_by_id(query.id)
        if not validation_rule:
            return None

        return ValidationRuleMapper.entity_to_dto(validation_rule)
