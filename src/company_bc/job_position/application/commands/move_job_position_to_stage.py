from dataclasses import dataclass
from typing import Optional, Dict, List, Any
from datetime import datetime, timedelta

from src.framework.application.command_bus import Command, CommandHandler
from src.company_bc.job_position.domain.exceptions import JobPositionNotFoundException
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_stage_id import JobPositionStageId
from src.company_bc.job_position.domain.value_objects.job_position_activity_id import JobPositionActivityId
from src.company_bc.job_position.domain.repositories.job_position_repository_interface import JobPositionRepositoryInterface
from src.company_bc.job_position.domain.infrastructure.job_position_stage_repository_interface import (
    JobPositionStageRepositoryInterface
)
from src.company_bc.job_position.domain.infrastructure.job_position_activity_repository_interface import (
    JobPositionActivityRepositoryInterface
)
from src.company_bc.job_position.domain.entities.job_position_stage import JobPositionStage
from src.company_bc.job_position.domain.entities.job_position_activity import JobPositionActivity
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId


class JobPositionValidationError(Exception):
    """Exception raised when job position validation fails"""
    def __init__(self, message: str, validation_errors: Dict[str, List[str]]):
        super().__init__(message)
        self.validation_errors = validation_errors


@dataclass
class MoveJobPositionToStageCommand(Command):
    """Command to move a job position to a new stage"""
    id: JobPositionId
    stage_id: StageId  # This is WorkflowStageId as string
    comment: Optional[str] = None  # Optional comment for the stage change
    user_id: Optional[str] = None  # Company user ID who is moving the stage


class MoveJobPositionToStageCommandHandler(CommandHandler[MoveJobPositionToStageCommand]):
    """Handler for moving a job position to a new stage"""

    def __init__(
        self,
        job_position_repository: JobPositionRepositoryInterface,
        workflow_repository: WorkflowRepositoryInterface,
        stage_repository: WorkflowStageRepositoryInterface,
        job_position_stage_repository: JobPositionStageRepositoryInterface,
        activity_repository: JobPositionActivityRepositoryInterface
    ):
        self.job_position_repository = job_position_repository
        self.workflow_repository = workflow_repository
        self.stage_repository = stage_repository
        self.job_position_stage_repository = job_position_stage_repository
        self.activity_repository = activity_repository

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

        # Convert StageId to WorkflowStageId
        workflow_stage_id = WorkflowStageId.from_string(command.stage_id.value)

        # Get the target stage from the new workflow system
        target_stage = self.stage_repository.get_by_id(workflow_stage_id)
        if not target_stage:
            raise JobPositionValidationError(
                "Stage not found",
                {"stage": [f"Stage {command.stage_id.value} not found"]}
            )

        # Verify the stage belongs to the workflow
        # Convert JobPositionWorkflowId to WorkflowId
        workflow_id = WorkflowId.from_string(job_position.job_position_workflow_id.value)
        workflow = self.workflow_repository.get_by_id(workflow_id)
        if not workflow:
            raise JobPositionValidationError(
                "Workflow not found",
                {"workflow": ["Associated workflow not found"]}
            )

        if target_stage.workflow_id.value != workflow.id.value:
            raise JobPositionValidationError(
                "Stage not in workflow",
                {"stage": [f"Stage {command.stage_id.value} does not belong to workflow {workflow.id.value}"]}
            )

        # Validate custom fields using JsonLogic validation rules
        if target_stage.validation_rules:
            validation_errors = self._validate_with_jsonlogic(
                job_position.custom_fields_values,
                target_stage.validation_rules
            )
            if validation_errors:
                raise JobPositionValidationError(
                    "Validation failed for target stage",
                    validation_errors
                )

        # Get old stage info before moving
        old_stage_id = job_position.stage_id.value if job_position.stage_id else None
        old_stage_name = None
        if old_stage_id:
            old_stage = self.stage_repository.get_by_id(WorkflowStageId.from_string(old_stage_id))
            if old_stage:
                old_stage_name = old_stage.name

        # Complete the current stage if it exists
        current_stage_record = self.job_position_stage_repository.get_current_by_job_position(command.id)
        if current_stage_record:
            current_stage_record.complete(comments=command.comment)
            self.job_position_stage_repository.save(current_stage_record)

        # Create a new stage record for the target stage
        new_stage_record = JobPositionStage.create(
            id=JobPositionStageId.generate(),
            job_position_id=command.id,
            workflow_id=workflow.id,
            stage_id=workflow_stage_id,
            phase_id=workflow.phase_id,
            comments=command.comment,
            estimated_cost=target_stage.estimated_cost,
            deadline=self._calculate_deadline(target_stage.deadline_days) if target_stage.deadline_days else None
        )
        self.job_position_stage_repository.save(new_stage_record)

        # Move job position to new stage
        job_position.move_to_stage(command.stage_id)

        self.job_position_repository.save(job_position)

        # Create activity log for stage move
        if command.user_id:
            try:
                activity_id = JobPositionActivityId.generate()
                user_id = CompanyUserId.from_string(command.user_id)
                activity = JobPositionActivity.from_stage_move(
                    id=activity_id,
                    job_position_id=command.id,
                    user_id=user_id,
                    old_stage_id=old_stage_id,
                    old_stage_name=old_stage_name,
                    new_stage_id=command.stage_id.value,
                    new_stage_name=target_stage.name
                )
                self.activity_repository.save(activity)
            except Exception as e:
                # Log error but don't fail the command if activity creation fails
                import logging
                logger = logging.getLogger(__name__)
                logger.error(f"Failed to create activity for stage move: {e}")

    def _validate_with_jsonlogic(
        self,
        field_values: Dict[str, Any],
        validation_rules: Dict[str, Any]
    ) -> Dict[str, List[str]]:
        """
        Validate custom field values against JsonLogic validation rules.
        
        TODO: Implement proper JsonLogic validation using a JsonLogic library.
        For now, this is a placeholder that returns no errors.
        In production, this should use a JsonLogic evaluator to validate the rules.
        
        Args:
            field_values: Current custom field values
            validation_rules: JsonLogic validation rules from stage
            
        Returns:
            Dict mapping field names to list of error messages
        """
        errors: Dict[str, List[str]] = {}
        
        # TODO: Implement JsonLogic validation
        # This requires installing a JsonLogic library (e.g., python-json-logic)
        # and evaluating the rules against field_values
        # For now, we skip validation to avoid breaking the flow
        # In production, implement proper JsonLogic evaluation here
        
        return errors

    def _calculate_deadline(self, deadline_days: int) -> datetime:
        """Calculate deadline datetime from days"""
        return datetime.utcnow() + timedelta(days=deadline_days)
