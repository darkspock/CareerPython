from dataclasses import dataclass
from typing import List

from src.shared.application.query_bus import Query
from src.shared.application.query_bus import QueryHandler
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface
from src.field_validation.application.dtos.validation_rule_dto import ValidationRuleDto
from src.field_validation.application.mappers.validation_rule_mapper import ValidationRuleMapper


@dataclass(frozen=True)
class ListValidationRulesByStageQuery(Query):
    """Query to list validation rules by stage."""

    stage_id: WorkflowStageId
    active_only: bool = False


class ListValidationRulesByStageQueryHandler(QueryHandler[ListValidationRulesByStageQuery, List[ValidationRuleDto]]):
    """Handler for listing validation rules by stage."""

    def __init__(self, repository: ValidationRuleRepositoryInterface):
        self.repository = repository

    def handle(self, query: ListValidationRulesByStageQuery) -> List[ValidationRuleDto]:
        """Handle the query."""
        validation_rules = self.repository.list_by_stage(
            stage_id=query.stage_id,
            active_only=query.active_only
        )

        return [ValidationRuleMapper.entity_to_dto(rule) for rule in validation_rules]
