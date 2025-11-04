import logging
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional, Dict, Any

from src.company.domain.value_objects.company_id import CompanyId
from src.job_position.domain.enums import JobPositionStatusEnum, JobPositionVisibilityEnum
from src.job_position.domain.exceptions.job_position_exceptions import JobPositionValidationError
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.job_position.domain.value_objects.stage_id import StageId
from src.shared.domain.enums.job_category import JobCategoryEnum


@dataclass
class JobPosition:
    """Job position domain entity - simplified version with custom fields"""
    id: JobPositionId
    title: str
    company_id: CompanyId
    job_position_workflow_id: Optional[JobPositionWorkflowId]  # Workflow system
    phase_workflows: Optional[Dict[str, str]]  # Phase 12.8: phase_id -> workflow_id mapping
    stage_id: Optional[StageId]  # Current stage in workflow
    custom_fields_values: Dict[str, Any]  # Custom field values (JSON) - contains all removed fields
    description: Optional[str]
    job_category: JobCategoryEnum
    open_at: Optional[datetime]
    application_deadline: Optional[date]
    visibility: JobPositionVisibilityEnum  # Visibility level (replaces is_public)
    public_slug: Optional[str]
    created_at: Optional[datetime]
    updated_at: Optional[datetime]

    def get_status(self) -> JobPositionStatusEnum:
        """
        Get the status from the current stage.
        
        The status is derived from the stage's status_mapping.
        If no workflow or stage is assigned, returns DRAFT as default.
        
        Returns:
            JobPositionStatusEnum: The status derived from the current stage
        """
        # TODO: This will be implemented when we have access to the workflow repository
        # to get the stage and its status_mapping. For now, return DRAFT as default.
        # This method should be called from the application layer where we have access
        # to the workflow repository.
        return JobPositionStatusEnum.DRAFT

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

    def can_receive_applications(self) -> bool:
        """
        Check if job position can receive applications.
        
        This is determined by the stage's status_mapping being ACTIVE.
        TODO: This will need access to the workflow repository to check the stage.
        """
        # TODO: Implement when we have access to workflow repository
        # Check if current stage's status_mapping is ACTIVE
        return False

    def get_workflow_for_phase(self, phase_id: str) -> Optional[str]:
        """Get the workflow ID configured for a specific phase

        Phase 12.8: Returns the workflow_id configured for the given phase.
        If no phase-specific workflow is configured, returns None.
        """
        if self.phase_workflows and phase_id in self.phase_workflows:
            return self.phase_workflows[phase_id]
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
