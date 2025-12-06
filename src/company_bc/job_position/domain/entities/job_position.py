from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.job_position.domain.enums import JobPositionStatusEnum, JobPositionVisibilityEnum
from src.company_bc.job_position.domain.exceptions.job_position_exceptions import JobPositionValidationError
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


@dataclass
class JobPosition:
    """Job position domain entity - simplified version with custom fields"""
    id: JobPositionId
    title: str
    company_id: CompanyId
    job_position_workflow_id: Optional[JobPositionWorkflowId]  # Workflow system
    phase_workflows: Optional[Dict[str, str]]  # Phase 12.8: phase_id -> workflow_id mapping
    stage_id: Optional[StageId]  # Current stage in workflow
    stage_assignments: Dict[str, list]  # Stage assignments: stage_id -> [company_user_id, ...]
    custom_fields_values: Dict[str, Any]  # Custom field values (JSON) - contains all removed fields
    description: Optional[str]
    job_category: JobCategoryEnum
    open_at: Optional[datetime]
    application_deadline: Optional[date]
    visibility: JobPositionVisibilityEnum  # Visibility level (replaces is_public)
    public_slug: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def move_to_stage(self, stage_id: StageId) -> None:
        """
        Move the job position to a new stage.

        Args:
            stage_id: The new stage ID

        Raises:
            JobPositionValidationError: If no workflow is assigned
        """
        if not self.job_position_workflow_id:
            raise JobPositionValidationError("Cannot move to stage without an assigned workflow")

        self.stage_id = stage_id
        self.updated_at = datetime.utcnow()

    def can_receive_applications(
            self,
            stage_type: Optional[str] = None
    ) -> bool:
        """
        Check if job position can receive applications.

        A job position can receive applications when:
        1. It has PUBLIC visibility
        2. Its current stage type is INITIAL or PROGRESS (active stages)

        Args:
            stage_type: The current stage's type (from WorkflowStageTypeEnum).
                       If not provided, only visibility is checked.

        Returns:
            True if the position can receive applications, False otherwise.

        Note:
            The stage_type should be obtained from the workflow stage repository
            and passed to this method by the calling service/command handler.
        """
        # Check visibility - must be PUBLIC to receive applications
        if self.visibility != JobPositionVisibilityEnum.PUBLIC:
            return False

        # If no stage type provided, check only visibility
        if stage_type is None:
            # Default to True if only checking visibility
            # The caller should provide stage_type for complete validation
            return True

        # Check if stage type allows receiving applications
        # Only INITIAL and PROGRESS stages can receive applications
        from src.shared_bc.customization.workflow.domain.enums.workflow_stage_type_enum import WorkflowStageTypeEnum
        active_stage_types = [
            WorkflowStageTypeEnum.INITIAL.value,
            WorkflowStageTypeEnum.PROGRESS.value
        ]
        return stage_type in active_stage_types

    def get_workflow_for_phase(self, phase_id: PhaseId) -> Optional[str]:
        """Get the workflow ID configured for a specific phase

        Phase 12.8: Returns the workflow_id configured for the given phase.
        If no phase-specific workflow is configured, returns None.
        """
        if self.phase_workflows and phase_id.value in self.phase_workflows:
            return self.phase_workflows[phase_id.value]
        return None

    def get_visible_custom_fields_for_candidate(
            self,
            stage_field_candidate_visibility: Optional[Dict[str, bool]] = None,
            default_field_candidate_visibility: Optional[Dict[str, bool]] = None
    ) -> Dict[str, Any]:
        """
        Get custom fields visible to candidates.

        Filters custom_fields_values based on visibility configuration from workflow/stage.

        Args:
            stage_field_candidate_visibility: Stage-specific visibility (from WorkflowStage)
            default_field_candidate_visibility: Default visibility (from JobPositionWorkflow.custom_fields_config)

        Returns:
            Dict[str, Any]: Filtered custom fields visible to candidates
        """
        visible_fields = {}

        for field_name, field_value in self.custom_fields_values.items():
            is_visible = False

            # First check stage-specific visibility
            if stage_field_candidate_visibility and field_name in stage_field_candidate_visibility:
                is_visible = stage_field_candidate_visibility[field_name]
            # Then check default visibility from workflow config
            elif default_field_candidate_visibility and field_name in default_field_candidate_visibility:
                is_visible = default_field_candidate_visibility[field_name]
            # Default to False if not specified
            else:
                is_visible = False

            if is_visible:
                visible_fields[field_name] = field_value

        return visible_fields

    def update_custom_fields_values(self, new_values: Dict[str, Any]) -> None:
        """
        Update custom fields values, merging with existing values.

        Args:
            new_values: Dictionary of field names to values to update
        """
        self.custom_fields_values.update(new_values)
        self.updated_at = datetime.utcnow()

    def assign_users_to_stage(self, stage_id: str, user_ids: list[str]) -> None:
        """
        Assign users to a specific stage.
        
        Args:
            stage_id: The stage ID
            user_ids: List of company_user_id to assign
        """
        self.stage_assignments[stage_id] = user_ids
        self.updated_at = datetime.utcnow()

    def add_user_to_stage(self, stage_id: str, user_id: str) -> None:
        """
        Add a user to a stage assignment.
        
        Args:
            stage_id: The stage ID
            user_id: The company_user_id to add
        """
        if stage_id not in self.stage_assignments:
            self.stage_assignments[stage_id] = []

        if user_id not in self.stage_assignments[stage_id]:
            self.stage_assignments[stage_id].append(user_id)
            self.updated_at = datetime.utcnow()

    def remove_user_from_stage(self, stage_id: str, user_id: str) -> None:
        """
        Remove a user from a stage assignment.
        
        Args:
            stage_id: The stage ID
            user_id: The company_user_id to remove
        """
        if stage_id in self.stage_assignments and user_id in self.stage_assignments[stage_id]:
            self.stage_assignments[stage_id].remove(user_id)
            self.updated_at = datetime.utcnow()

    def get_stage_assigned_users(self, stage_id: str) -> list[str]:
        """
        Get users assigned to a specific stage.
        
        Args:
            stage_id: The stage ID
            
        Returns:
            List of company_user_ids assigned to the stage
        """
        return self.stage_assignments.get(stage_id, [])

    def update_details(
            self,
            title: str,
            description: Optional[str],
            job_category: JobCategoryEnum,
            open_at: Optional[datetime],
            application_deadline: Optional[date],
            job_position_workflow_id: Optional[JobPositionWorkflowId] = None,
            stage_id: Optional[StageId] = None,
            phase_workflows: Optional[Dict[str, str]] = None,
            custom_fields_values: Optional[Dict[str, Any]] = None,
            visibility: Optional[JobPositionVisibilityEnum] = None,
            public_slug: Optional[str] = None
    ) -> None:
        """Update job position details with all attributes"""
        # Validate required fields
        if not title or title.strip() == "":
            raise JobPositionValidationError("Title is required")

        if job_position_workflow_id is not None:
            self.job_position_workflow_id = job_position_workflow_id
        if stage_id is not None:
            self.stage_id = stage_id
        if phase_workflows is not None:
            self.phase_workflows = phase_workflows
        if custom_fields_values is not None:
            self.custom_fields_values.update(custom_fields_values)
        if visibility is not None:
            self.visibility = visibility
        if public_slug is not None:
            self.public_slug = public_slug

        self.title = title.strip()
        self.description = description
        self.job_category = job_category
        self.open_at = open_at
        self.application_deadline = application_deadline
        self.updated_at = datetime.utcnow()

    @staticmethod
    def create(
            id: JobPositionId,
            title: str,
            company_id: CompanyId,
            job_position_workflow_id: Optional[JobPositionWorkflowId] = None,
            stage_id: Optional[StageId] = None,
            phase_workflows: Optional[Dict[str, str]] = None,
            custom_fields_values: Optional[Dict[str, Any]] = None,
            description: Optional[str] = None,
            job_category: JobCategoryEnum = JobCategoryEnum.OTHER,
            open_at: Optional[datetime] = None,
            application_deadline: Optional[date] = None,
            visibility: JobPositionVisibilityEnum = JobPositionVisibilityEnum.HIDDEN,
            public_slug: Optional[str] = None,
    ) -> 'JobPosition':
        """Create a new job position"""
        if not title or title.strip() == "":
            raise JobPositionValidationError("Title is required")

        now = datetime.utcnow()

        return JobPosition(
            id=id,
            title=title.strip(),
            company_id=company_id,
            job_position_workflow_id=job_position_workflow_id,
            stage_id=stage_id,
            phase_workflows=phase_workflows or {},
            stage_assignments={},  # Initialize empty stage assignments
            custom_fields_values=custom_fields_values or {},
            description=description,
            job_category=job_category,
            open_at=open_at,
            application_deadline=application_deadline,
            visibility=visibility,
            public_slug=public_slug,
            created_at=now,
            updated_at=now
        )

    @classmethod
    def _from_repository(
            cls,
            id: JobPositionId,
            title: str,
            company_id: CompanyId,
            job_position_workflow_id: Optional[JobPositionWorkflowId],
            stage_id: Optional[StageId],
            phase_workflows: Optional[Dict[str, str]],
            stage_assignments: Optional[Dict[str, list]],
            custom_fields_values: Optional[Dict[str, Any]],
            description: Optional[str],
            job_category: JobCategoryEnum,
            open_at: Optional[datetime],
            application_deadline: Optional[date],
            visibility: JobPositionVisibilityEnum,
            public_slug: Optional[str],
            created_at: datetime,
            updated_at: datetime,
    ) -> 'JobPosition':
        """Create JobPosition from repository data - only for repositories to use"""
        return cls(
            id=id,
            title=title,
            company_id=company_id,
            job_position_workflow_id=job_position_workflow_id,
            stage_id=stage_id,
            phase_workflows=phase_workflows or {},
            stage_assignments=stage_assignments or {},
            custom_fields_values=custom_fields_values or {},
            description=description,
            job_category=job_category,
            open_at=open_at,
            application_deadline=application_deadline,
            visibility=visibility,
            public_slug=public_slug,
            created_at=created_at,
            updated_at=updated_at
        )
