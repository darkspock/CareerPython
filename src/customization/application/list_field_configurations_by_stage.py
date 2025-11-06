from dataclasses import dataclass
from typing import List

from src.customization.application.field_configuration_dto import FieldConfigurationDto
from src.customization.application.field_configuration_mapper import FieldConfigurationMapper
from src.workflow.domain.infrastructure.field_configuration_repository_interface import FieldConfigurationRepositoryInterface
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListFieldConfigurationsByStageQuery(Query):
    """Query to list all field configurations for a stage"""
    stage_id: str


class ListFieldConfigurationsByStageQueryHandler(QueryHandler[ListFieldConfigurationsByStageQuery, List[FieldConfigurationDto]]):
    def __init__(self, repository: FieldConfigurationRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListFieldConfigurationsByStageQuery) -> List[FieldConfigurationDto]:
        stage_id = WorkflowStageId.from_string(query.stage_id)
        field_configurations = self._repository.list_by_stage(stage_id)
        return [FieldConfigurationMapper.entity_to_dto(config) for config in field_configurations]
