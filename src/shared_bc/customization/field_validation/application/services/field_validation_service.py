from typing import Dict, Any, Optional, List

from src.customization.domain.interfaces import CustomFieldRepositoryInterface
from src.shared_bc.customization.field_validation.domain.infrastructure.validation_rule_repository_interface import ValidationRuleRepositoryInterface
from src.shared_bc.customization.field_validation.application.dtos.stage_validation_result_dto import StageValidationResultDto, ValidationIssueDto
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class FieldValidationService:
    """Service for validating custom field values against validation rules."""

    def __init__(
        self,
        validation_rule_repository: ValidationRuleRepositoryInterface,
        custom_field_repository: CustomFieldRepositoryInterface
    ):
        self.validation_rule_repository = validation_rule_repository
        self.custom_field_repository = custom_field_repository

    def validate_stage_transition(
        self,
        stage_id: WorkflowStageId,
        candidate_field_values: Dict[str, Any],
        position_data: Optional[Dict[str, Any]] = None
    ) -> StageValidationResultDto:
        """
        Validate all custom field values for a stage transition.

        Args:
            stage_id: The workflow stage ID
            candidate_field_values: Dict mapping custom_field_id to candidate's value
            position_data: Optional position data for comparison rules

        Returns:
            StageValidationResultDto with all validation results
        """
        # Get all active validation rules for this stage
        validation_rules = self.validation_rule_repository.list_by_stage(
            stage_id=stage_id,
            active_only=True
        )

        # If no rules, validation passes
        if not validation_rules:
            return StageValidationResultDto.success()

        # Get custom field information for field names
        field_ids = [rule.custom_field_id for rule in validation_rules]
        custom_fields_map = {}
        for field_id in field_ids:
            field = self.custom_field_repository.get_by_id(field_id)
            if field:
                custom_fields_map[str(field_id)] = field

        errors: List[ValidationIssueDto] = []
        warnings: List[ValidationIssueDto] = []

        # Evaluate each rule
        for rule in validation_rules:
            field_id_str = str(rule.custom_field_id)

            # Get candidate value for this field
            candidate_value = candidate_field_values.get(field_id_str)

            # Get field name
            custom_field = custom_fields_map.get(field_id_str)
            field_name = custom_field.field_name if custom_field else field_id_str

            # Evaluate the rule
            result = rule.evaluate(
                field_name=field_name,
                candidate_value=candidate_value,
                position=position_data
            )

            # Skip if validation passed
            if result.is_valid:
                continue

            # Create validation issue
            issue = ValidationIssueDto(
                field_key=field_id_str,
                field_name=field_name,
                message=result.message,
                severity=result.severity.value,
                rule_id=result.rule_id,
                should_auto_reject=result.should_auto_reject,
                rejection_reason=result.rejection_reason
            )

            # Add to appropriate list
            if result.is_error():
                errors.append(issue)
            elif result.is_warning():
                warnings.append(issue)

        # Return aggregated result
        if not errors and not warnings:
            return StageValidationResultDto.success()

        return StageValidationResultDto.with_issues(errors=errors, warnings=warnings)

    def validate_single_field(
        self,
        stage_id: WorkflowStageId,
        custom_field_id: str,
        candidate_value: Any,
        position_data: Optional[Dict[str, Any]] = None
    ) -> StageValidationResultDto:
        """
        Validate a single custom field value.

        Args:
            stage_id: The workflow stage ID
            custom_field_id: The custom field ID
            candidate_value: The candidate's value for this field
            position_data: Optional position data for comparison rules

        Returns:
            StageValidationResultDto with validation results for this field
        """
        return self.validate_stage_transition(
            stage_id=stage_id,
            candidate_field_values={custom_field_id: candidate_value},
            position_data=position_data
        )
