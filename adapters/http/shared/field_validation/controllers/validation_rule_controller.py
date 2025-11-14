from typing import List, Optional

from adapters.http.shared.field_validation.mappers.validation_rule_mapper import ValidationRuleResponseMapper, \
    ValidationResultResponseMapper
from adapters.http.shared.field_validation.schemas.create_validation_rule_request import CreateValidationRuleRequest
from adapters.http.shared.field_validation.schemas.update_validation_rule_request import UpdateValidationRuleRequest
from adapters.http.shared.field_validation.schemas.validation_rule_response import ValidationRuleResponse
from src.shared_bc.customization.entity_customization.domain.value_objects.custom_field_id import CustomFieldId
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus
from src.shared_bc.customization.field_validation.application.dtos.validation_rule_dto import ValidationRuleDto
from src.shared_bc.customization.field_validation.domain.value_objects.validation_rule_id import ValidationRuleId
from src.shared_bc.customization.field_validation.domain.enums import ValidationRuleType
from src.shared_bc.customization.field_validation.domain.enums.comparison_operator import ComparisonOperator
from src.shared_bc.customization.field_validation.domain.enums import ValidationSeverity
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.shared_bc.customization.field_validation.application.commands.create_validation_rule_command import CreateValidationRuleCommand
from src.shared_bc.customization.field_validation.application.commands.update_validation_rule_command import UpdateValidationRuleCommand
from src.shared_bc.customization.field_validation.application.commands.delete_validation_rule_command import DeleteValidationRuleCommand
from src.shared_bc.customization.field_validation.application.commands.activate_validation_rule_command import ActivateValidationRuleCommand
from src.shared_bc.customization.field_validation.application.commands.deactivate_validation_rule_command import DeactivateValidationRuleCommand
from src.shared_bc.customization.field_validation.application.queries.get_validation_rule_by_id_query import GetValidationRuleByIdQuery
from src.shared_bc.customization.field_validation.application.queries.list_validation_rules_by_stage_query import ListValidationRulesByStageQuery
from src.shared_bc.customization.field_validation.application.queries.list_validation_rules_by_field_query import ListValidationRulesByFieldQuery
from src.shared_bc.customization.field_validation.application.services.field_validation_service import FieldValidationService
from adapters.http.shared.field_validation.schemas.validate_stage_request import ValidateStageRequest
from adapters.http.shared.field_validation.schemas.validation_result_response import ValidationResultResponse


class ValidationRuleController:
    """Controller for validation rule operations."""

    def __init__(
        self,
        command_bus: CommandBus,
        query_bus: QueryBus,
        validation_service: FieldValidationService
    ):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.validation_service = validation_service

    def create_validation_rule(self, request: CreateValidationRuleRequest) -> ValidationRuleResponse:
        """Create a new validation rule."""
        rule_id = ValidationRuleId.generate()

        command = CreateValidationRuleCommand(
            id=rule_id,
            custom_field_id=CustomFieldId.from_string(request.custom_field_id),
            stage_id=WorkflowStageId.from_string(request.stage_id),
            rule_type=ValidationRuleType(request.rule_type),
            comparison_operator=ComparisonOperator(request.comparison_operator),
            severity=ValidationSeverity(request.severity),
            validation_message=request.validation_message,
            position_field_path=request.position_field_path,
            comparison_value=request.comparison_value,
            auto_reject=request.auto_reject,
            rejection_reason=request.rejection_reason,
            is_active=request.is_active
        )

        self.command_bus.execute(command)

        # Query the created rule
        query = GetValidationRuleByIdQuery(id=rule_id)
        dto: Optional[ValidationRuleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError("Failed to retrieve created validation rule")

        return ValidationRuleResponseMapper.dto_to_response(dto)

    def get_validation_rule(self, rule_id: str) -> ValidationRuleResponse:
        """Get a validation rule by ID."""
        query = GetValidationRuleByIdQuery(id=ValidationRuleId.from_string(rule_id))
        dto: Optional[ValidationRuleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError(f"Validation rule {rule_id} not found")

        return ValidationRuleResponseMapper.dto_to_response(dto)

    def list_validation_rules_by_stage(self, stage_id: str, active_only: bool = False) -> List[ValidationRuleResponse]:
        """List all validation rules for a stage."""
        query = ListValidationRulesByStageQuery(
            stage_id=WorkflowStageId.from_string(stage_id),
            active_only=active_only
        )
        dtos: List[ValidationRuleDto] = self.query_bus.query(query)

        return [ValidationRuleResponseMapper.dto_to_response(dto) for dto in dtos]

    def list_validation_rules_by_field(self, custom_field_id: str, active_only: bool = False) -> List[ValidationRuleResponse]:
        """List all validation rules for a custom field."""
        query = ListValidationRulesByFieldQuery(
            custom_field_id=CustomFieldId.from_string(custom_field_id),
            active_only=active_only
        )
        dtos: List[ValidationRuleDto] = self.query_bus.query(query)

        return [ValidationRuleResponseMapper.dto_to_response(dto) for dto in dtos]

    def update_validation_rule(self, rule_id: str, request: UpdateValidationRuleRequest) -> ValidationRuleResponse:
        """Update a validation rule."""
        command = UpdateValidationRuleCommand(
            id=ValidationRuleId.from_string(rule_id),
            comparison_operator=ComparisonOperator(request.comparison_operator),
            severity=ValidationSeverity(request.severity),
            validation_message=request.validation_message,
            position_field_path=request.position_field_path,
            comparison_value=request.comparison_value,
            auto_reject=request.auto_reject,
            rejection_reason=request.rejection_reason,
            is_active=request.is_active
        )

        self.command_bus.execute(command)

        # Query the updated rule
        query = GetValidationRuleByIdQuery(id=ValidationRuleId.from_string(rule_id))
        dto: Optional[ValidationRuleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError("Failed to retrieve updated validation rule")

        return ValidationRuleResponseMapper.dto_to_response(dto)

    def delete_validation_rule(self, rule_id: str) -> None:
        """Delete a validation rule."""
        command = DeleteValidationRuleCommand(id=ValidationRuleId.from_string(rule_id))
        self.command_bus.execute(command)

    def activate_validation_rule(self, rule_id: str) -> ValidationRuleResponse:
        """Activate a validation rule."""
        command = ActivateValidationRuleCommand(id=ValidationRuleId.from_string(rule_id))
        self.command_bus.execute(command)

        # Query the updated rule
        query = GetValidationRuleByIdQuery(id=ValidationRuleId.from_string(rule_id))
        dto: Optional[ValidationRuleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError("Failed to retrieve validation rule")

        return ValidationRuleResponseMapper.dto_to_response(dto)

    def deactivate_validation_rule(self, rule_id: str) -> ValidationRuleResponse:
        """Deactivate a validation rule."""
        command = DeactivateValidationRuleCommand(id=ValidationRuleId.from_string(rule_id))
        self.command_bus.execute(command)

        # Query the updated rule
        query = GetValidationRuleByIdQuery(id=ValidationRuleId.from_string(rule_id))
        dto: Optional[ValidationRuleDto] = self.query_bus.query(query)

        if not dto:
            raise ValueError("Failed to retrieve validation rule")

        return ValidationRuleResponseMapper.dto_to_response(dto)

    def validate_stage_transition(self, request: ValidateStageRequest) -> ValidationResultResponse:
        """Validate a stage transition."""
        result_dto = self.validation_service.validate_stage_transition(
            stage_id=WorkflowStageId.from_string(request.stage_id),
            candidate_field_values=request.candidate_field_values,
            position_data=request.position_data
        )

        return ValidationResultResponseMapper.dto_to_response(result_dto)
