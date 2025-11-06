from dataclasses import dataclass
from typing import Optional, Dict, List, Any

from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.infrastructure.job_position_workflow_repository_interface import (
    JobPositionWorkflowRepositoryInterface
)
from src.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.job_position.domain.value_objects.stage_id import StageId
from src.shared.application.command_bus import Command, CommandHandler


class JobPositionValidationError(Exception):
    """Exception raised when job position validation fails"""

    def __init__(self, message: str, validation_errors: Dict[str, List[str]]):
        super().__init__(message)
        self.validation_errors = validation_errors


@dataclass
class MoveJobPositionToStageCommand(Command):
    """Command to move a job position to a new stage"""
    id: JobPositionId
    stage_id: StageId
    comment: Optional[str] = None  # Optional comment for the stage change


class MoveJobPositionToStageCommandHandler(CommandHandler[MoveJobPositionToStageCommand]):
    """Handler for moving a job position to a new stage"""

    def __init__(
            self,
            job_position_repository: JobPositionRepositoryInterface,
            workflow_repository: JobPositionWorkflowRepositoryInterface
    ):
        self.job_position_repository = job_position_repository
        self.workflow_repository = workflow_repository

    def execute(self, command: MoveJobPositionToStageCommand) -> None:
        """Execute the command - moves job position to new stage"""
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        # Get the workflow to access stage configuration
        if not job_position.job_position_workflow_id:
            raise JobPositionValidationError(
                "Cannot move position without workflow",
                {"workflow": ["Job position must have an assigned workflow"]}
            )

        workflow = self.workflow_repository.get_by_id(job_position.job_position_workflow_id)
        if not workflow:
            raise JobPositionValidationError(
                "Workflow not found",
                {"workflow": ["Associated workflow not found"]}
            )

        # Find the target stage
        target_stage = workflow.get_stage_by_id(command.stage_id.value)
        if not target_stage:
            raise JobPositionValidationError(
                "Stage not found",
                {"stage": [f"Stage {command.stage_id.value} not found in workflow"]}
            )

        # Validate custom fields for the target stage
        validation_errors = self._validate_custom_fields(
            job_position.custom_fields_values,
            target_stage.field_validation,
            workflow.custom_fields_config
        )

        if validation_errors:
            raise JobPositionValidationError(
                "Validation failed for target stage",
                validation_errors
            )

        # Move to new stage
        job_position.move_to_stage(command.stage_id)

        self.job_position_repository.save(job_position)

    def _validate_custom_fields(
            self,
            field_values: Dict[str, Any],
            field_validation: Dict[str, Any],
            custom_fields_config: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Validate custom field values against stage validation rules.

        Args:
            field_values: Current custom field values
            field_validation: Validation configuration from stage
            custom_fields_config: Custom fields definition from workflow

        Returns:
            Dict mapping field names to list of error messages
        """
        errors: Dict[str, List[str]] = {}

        # Check each field's validation requirements
        for field_name, validation_rule in field_validation.items():
            # Get the field value
            field_value = field_values.get(field_name)

            # Get field configuration
            field_config = custom_fields_config.get(field_name, {})
            field_label = field_config.get('label', field_name)

            # Check validation rule
            if isinstance(validation_rule, str):
                # Simple string validation: 'required', 'optional', 'recommended'
                if validation_rule == 'required' or validation_rule == 'requerido':
                    if field_value is None or field_value == '' or field_value == []:
                        if field_name not in errors:
                            errors[field_name] = []
                        errors[field_name].append(f"{field_label} is required for this stage")
            elif isinstance(validation_rule, dict):
                # Complex validation rule with multiple checks
                is_required = validation_rule.get('required', False) or validation_rule.get('requerido', False)
                if is_required:
                    if field_value is None or field_value == '' or field_value == []:
                        if field_name not in errors:
                            errors[field_name] = []
                        errors[field_name].append(f"{field_label} is required for this stage")

        return errors
