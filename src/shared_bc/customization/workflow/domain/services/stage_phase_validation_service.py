"""
Domain Service for validating stage-phase consistency.

This is a Domain Service because it encapsulates business rules that require
access to multiple domain entities through repositories. The logic belongs to
the domain, not the application layer.
"""
from typing import Optional

from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.domain.interfaces.workflow_repository_interface import \
    WorkflowRepositoryInterface
from src.shared_bc.customization.workflow.domain.interfaces.workflow_stage_repository_interface import \
    WorkflowStageRepositoryInterface
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class StagePhaseValidationService:
    """
    Domain Service for validating stage-phase consistency rules.
    
    This service encapsulates the business rule that a stage must belong to
    a workflow that belongs to a phase. It's a Domain Service because:
    - It contains domain logic (business rules)
    - It requires access to repositories to validate across entities
    - It's called from Application Layer (Command Handlers) but the logic is domain logic
    """

    def __init__(
            self,
            workflow_repository: WorkflowRepositoryInterface,
            stage_repository: WorkflowStageRepositoryInterface
    ):
        self.workflow_repository = workflow_repository
        self.stage_repository = stage_repository

    def validate_stage_belongs_to_phase(
            self,
            stage_id: WorkflowStageId,
            expected_phase_id: Optional[PhaseId] = None
    ) -> tuple[WorkflowId, PhaseId]:
        """
        Validate that a stage belongs to a workflow that belongs to a phase.
        
        Business Rules:
        1. Stage must exist
        2. Stage must belong to a workflow
        3. Workflow must have a phase_id (cannot be None)
        4. If expected_phase_id is provided, it must match the workflow's phase_id
        
        Args:
            stage_id: The stage ID to validate
            expected_phase_id: Optional phase ID to check against
            
        Returns:
            Tuple of (workflow_id, phase_id) if valid
            
        Raises:
            ValueError: If validation fails with descriptive message
        """
        # Get stage
        stage = self.stage_repository.get_by_id(stage_id)
        if not stage:
            raise ValueError(f"Stage {stage_id.value} not found")

        # Get workflow
        workflow = self.workflow_repository.get_by_id(stage.workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {stage.workflow_id.value} not found for stage {stage_id.value}")

        # Validate workflow has phase_id (Business Rule: workflow must belong to a phase)
        if not workflow.phase_id:
            raise ValueError(f"Workflow {workflow.id.value} must belong to a phase")

        # Validate phase_id matches if expected
        if expected_phase_id:
            if workflow.phase_id.value != expected_phase_id.value:
                raise ValueError(
                    f"Stage {stage_id.value} belongs to workflow in phase {workflow.phase_id.value}, "
                    f"but expected phase is {expected_phase_id.value}"
                )

        return (workflow.id, workflow.phase_id)

    def validate_stage_belongs_to_workflow(
            self,
            stage_id: WorkflowStageId,
            workflow_id: WorkflowId
    ) -> None:
        """
        Validate that a stage belongs to a specific workflow.
        
        Business Rules:
        1. Stage must exist
        2. Stage must belong to the specified workflow
        
        Args:
            stage_id: The stage ID to validate
            workflow_id: The workflow ID to check against
            
        Raises:
            ValueError: If validation fails with descriptive message
        """
        stage = self.stage_repository.get_by_id(stage_id)
        if not stage:
            raise ValueError(f"Stage {stage_id.value} not found")

        if stage.workflow_id.value != workflow_id.value:
            raise ValueError(
                f"Stage {stage_id.value} does not belong to workflow {workflow_id.value}"
            )

    def validate_workflow_has_phase(
            self,
            workflow_id: WorkflowId
    ) -> PhaseId:
        """
        Validate that a workflow belongs to a phase.
        
        Business Rule: Every workflow must belong to a phase.
        
        Args:
            workflow_id: The workflow ID to validate
            
        Returns:
            PhaseId if valid
            
        Raises:
            ValueError: If workflow doesn't exist or doesn't have a phase_id
        """
        workflow = self.workflow_repository.get_by_id(workflow_id)
        if not workflow:
            raise ValueError(f"Workflow {workflow_id.value} not found")

        if not workflow.phase_id:
            raise ValueError(f"Workflow {workflow_id.value} must belong to a phase")

        return workflow.phase_id
