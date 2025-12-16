from dataclasses import dataclass, field
from datetime import datetime, date
from decimal import Decimal
from typing import Optional, Dict, Any, List

from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.job_position.domain.enums import (
    JobPositionStatusEnum,
    JobPositionVisibilityEnum,
    EmploymentTypeEnum,
    ExperienceLevelEnum,
    WorkLocationTypeEnum,
    ClosedReasonEnum,
    SalaryPeriodEnum,
    ApplicationModeEnum,
)
from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
    JobPositionValidationError,
    JobPositionInvalidStatusTransitionError,
    JobPositionFieldLockedError,
    JobPositionBudgetExceededError,
)
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.company_bc.job_position.domain.value_objects.job_position_workflow_id import JobPositionWorkflowId
from src.company_bc.job_position.domain.value_objects.stage_id import StageId
from src.company_bc.job_position.domain.value_objects.language_requirement import LanguageRequirement
from src.company_bc.job_position.domain.value_objects.custom_field_definition import CustomFieldDefinition
from src.framework.domain.enums.job_category import JobCategoryEnum
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId


@dataclass
class JobPosition:
    """Job position domain entity with publishing flow support"""
    # Core identification
    id: JobPositionId
    title: str
    company_id: CompanyId

    # Workflow system - Publication (PO)
    job_position_workflow_id: Optional[JobPositionWorkflowId]  # Publication workflow (PO)
    phase_workflows: Optional[Dict[str, str]]  # phase_id -> workflow_id mapping
    stage_id: Optional[StageId]  # Current stage in publication workflow
    stage_assignments: Dict[str, list]  # stage_id -> [company_user_id, ...]

    # Workflow system - Candidate Application (CA)
    candidate_application_workflow_id: Optional[str]  # Hiring pipeline workflow (CA) for candidates

    # Content fields
    description: Optional[str]
    job_category: JobCategoryEnum
    skills: List[str]
    languages: List[LanguageRequirement]

    # Standard fields
    department_id: Optional[str]
    employment_type: Optional[EmploymentTypeEnum]
    experience_level: Optional[ExperienceLevelEnum]
    work_location_type: Optional[WorkLocationTypeEnum]
    office_locations: List[str]
    remote_restrictions: Optional[str]
    number_of_openings: int
    requisition_id: Optional[str]

    # Financial fields
    salary_currency: Optional[str]
    salary_min: Optional[Decimal]
    salary_max: Optional[Decimal]
    salary_period: Optional[SalaryPeriodEnum]
    show_salary: bool
    budget_max: Optional[Decimal]
    approved_budget_max: Optional[Decimal]
    financial_approver_id: Optional[CompanyUserId]
    approved_at: Optional[datetime]

    # Ownership fields
    hiring_manager_id: Optional[CompanyUserId]
    recruiter_id: Optional[CompanyUserId]
    created_by_id: Optional[CompanyUserId]

    # Lifecycle / Publishing flow fields
    status: JobPositionStatusEnum
    closed_reason: Optional[ClosedReasonEnum]
    closed_at: Optional[datetime]
    published_at: Optional[datetime]

    # Custom fields snapshot (copied from workflow at creation, frozen at publish)
    custom_fields_config: List[CustomFieldDefinition]
    custom_fields_values: Dict[str, Any]
    source_workflow_id: Optional[str]

    # Pipeline references
    candidate_pipeline_id: Optional[str]

    # Screening reference (for interview template)
    screening_template_id: Optional[str]

    # Killer questions (simple inline questions stored as JSON)
    # Format: List[{name: str, description?: str, data_type: str, scoring_values?: List[{label, scoring}], is_killer?: bool}]
    killer_questions: List[Dict[str, Any]]

    # Application configuration
    application_mode: ApplicationModeEnum  # SHORT, FULL, or CV_BUILDER
    required_sections: List[str]  # Sections required when application_mode is FULL: ['experience', 'education', 'skills', 'projects']

    # Visibility and publishing
    visibility: JobPositionVisibilityEnum
    public_slug: Optional[str]
    open_at: Optional[datetime]
    application_deadline: Optional[date]

    # Timestamps
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
            public_slug: Optional[str] = None,
            # New fields for publishing flow
            skills: Optional[List[str]] = None,
            languages: Optional[List[LanguageRequirement]] = None,
            department_id: Optional[str] = None,
            employment_type: Optional[EmploymentTypeEnum] = None,
            experience_level: Optional[ExperienceLevelEnum] = None,
            work_location_type: Optional[WorkLocationTypeEnum] = None,
            office_locations: Optional[List[str]] = None,
            remote_restrictions: Optional[str] = None,
            number_of_openings: Optional[int] = None,
            requisition_id: Optional[str] = None,
            salary_currency: Optional[str] = None,
            salary_min: Optional[Decimal] = None,
            salary_max: Optional[Decimal] = None,
            salary_period: Optional[SalaryPeriodEnum] = None,
            show_salary: Optional[bool] = None,
            budget_max: Optional[Decimal] = None,
            hiring_manager_id: Optional[CompanyUserId] = None,
            recruiter_id: Optional[CompanyUserId] = None,
            candidate_pipeline_id: Optional[str] = None,
            screening_template_id: Optional[str] = None,
            custom_fields_config: Optional[List[CustomFieldDefinition]] = None,
            killer_questions: Optional[List[Dict[str, Any]]] = None,
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

        # Update new fields if provided
        if skills is not None:
            self.skills = skills
        if languages is not None:
            self.languages = languages
        if department_id is not None:
            self.department_id = department_id
        if employment_type is not None:
            self.employment_type = employment_type
        if experience_level is not None:
            self.experience_level = experience_level
        if work_location_type is not None:
            self.work_location_type = work_location_type
        if office_locations is not None:
            self.office_locations = office_locations
        if remote_restrictions is not None:
            self.remote_restrictions = remote_restrictions
        if number_of_openings is not None:
            self.number_of_openings = number_of_openings
        if requisition_id is not None:
            self.requisition_id = requisition_id
        if salary_currency is not None:
            self.salary_currency = salary_currency
        if salary_min is not None:
            self.salary_min = salary_min
        if salary_max is not None:
            self.salary_max = salary_max
        if salary_period is not None:
            self.salary_period = salary_period
        if show_salary is not None:
            self.show_salary = show_salary
        if budget_max is not None:
            self.budget_max = budget_max
        if hiring_manager_id is not None:
            self.hiring_manager_id = hiring_manager_id
        if recruiter_id is not None:
            self.recruiter_id = recruiter_id
        if candidate_pipeline_id is not None:
            self.candidate_pipeline_id = candidate_pipeline_id
        if screening_template_id is not None:
            self.screening_template_id = screening_template_id
        if custom_fields_config is not None:
            self.custom_fields_config = custom_fields_config
        if killer_questions is not None:
            self.killer_questions = killer_questions

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
            # Workflow system - Publication (PO)
            job_position_workflow_id: Optional[JobPositionWorkflowId] = None,
            stage_id: Optional[StageId] = None,
            phase_workflows: Optional[Dict[str, str]] = None,
            # Workflow system - Candidate Application (CA)
            candidate_application_workflow_id: Optional[str] = None,
            # Content fields
            description: Optional[str] = None,
            job_category: JobCategoryEnum = JobCategoryEnum.OTHER,
            skills: Optional[List[str]] = None,
            languages: Optional[List[LanguageRequirement]] = None,
            # Standard fields
            department_id: Optional[str] = None,
            employment_type: Optional[EmploymentTypeEnum] = None,
            experience_level: Optional[ExperienceLevelEnum] = None,
            work_location_type: Optional[WorkLocationTypeEnum] = None,
            office_locations: Optional[List[str]] = None,
            remote_restrictions: Optional[str] = None,
            number_of_openings: int = 1,
            requisition_id: Optional[str] = None,
            # Financial fields
            salary_currency: Optional[str] = None,
            salary_min: Optional[Decimal] = None,
            salary_max: Optional[Decimal] = None,
            salary_period: Optional[SalaryPeriodEnum] = None,
            show_salary: bool = False,
            budget_max: Optional[Decimal] = None,
            # Ownership fields
            hiring_manager_id: Optional[CompanyUserId] = None,
            recruiter_id: Optional[CompanyUserId] = None,
            created_by_id: Optional[CompanyUserId] = None,
            # Custom fields
            custom_fields_config: Optional[List[CustomFieldDefinition]] = None,
            custom_fields_values: Optional[Dict[str, Any]] = None,
            source_workflow_id: Optional[str] = None,
            # Pipeline and screening
            candidate_pipeline_id: Optional[str] = None,
            screening_template_id: Optional[str] = None,
            killer_questions: Optional[List[Dict[str, Any]]] = None,
            # Application configuration
            application_mode: ApplicationModeEnum = ApplicationModeEnum.SHORT,
            required_sections: Optional[List[str]] = None,
            # Visibility and publishing
            visibility: JobPositionVisibilityEnum = JobPositionVisibilityEnum.HIDDEN,
            public_slug: Optional[str] = None,
            open_at: Optional[datetime] = None,
            application_deadline: Optional[date] = None,
    ) -> 'JobPosition':
        """Create a new job position in DRAFT status"""
        if not title or title.strip() == "":
            raise JobPositionValidationError("Title is required")

        now = datetime.utcnow()

        return JobPosition(
            id=id,
            title=title.strip(),
            company_id=company_id,
            # Workflow system - Publication (PO)
            job_position_workflow_id=job_position_workflow_id,
            phase_workflows=phase_workflows or {},
            stage_id=stage_id,
            stage_assignments={},
            # Workflow system - Candidate Application (CA)
            candidate_application_workflow_id=candidate_application_workflow_id,
            # Content fields
            description=description,
            job_category=job_category,
            skills=skills or [],
            languages=languages or [],
            # Standard fields
            department_id=department_id,
            employment_type=employment_type,
            experience_level=experience_level,
            work_location_type=work_location_type,
            office_locations=office_locations or [],
            remote_restrictions=remote_restrictions,
            number_of_openings=number_of_openings,
            requisition_id=requisition_id,
            # Financial fields
            salary_currency=salary_currency,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_period=salary_period,
            show_salary=show_salary,
            budget_max=budget_max,
            approved_budget_max=None,
            financial_approver_id=None,
            approved_at=None,
            # Ownership fields
            hiring_manager_id=hiring_manager_id,
            recruiter_id=recruiter_id,
            created_by_id=created_by_id,
            # Lifecycle - new positions start in DRAFT
            status=JobPositionStatusEnum.DRAFT,
            closed_reason=None,
            closed_at=None,
            published_at=None,
            # Custom fields
            custom_fields_config=custom_fields_config or [],
            custom_fields_values=custom_fields_values or {},
            source_workflow_id=source_workflow_id,
            # Pipeline and screening
            candidate_pipeline_id=candidate_pipeline_id,
            screening_template_id=screening_template_id,
            killer_questions=killer_questions or [],
            # Application configuration
            application_mode=application_mode,
            required_sections=required_sections or [],
            # Visibility and publishing
            visibility=visibility,
            public_slug=public_slug,
            open_at=open_at,
            application_deadline=application_deadline,
            # Timestamps
            created_at=now,
            updated_at=now
        )

    @classmethod
    def _from_repository(
            cls,
            id: JobPositionId,
            title: str,
            company_id: CompanyId,
            # Workflow system - Publication (PO)
            job_position_workflow_id: Optional[JobPositionWorkflowId],
            phase_workflows: Optional[Dict[str, str]],
            stage_id: Optional[StageId],
            stage_assignments: Optional[Dict[str, list]],
            # Workflow system - Candidate Application (CA)
            candidate_application_workflow_id: Optional[str],
            # Content fields
            description: Optional[str],
            job_category: JobCategoryEnum,
            skills: Optional[List[str]],
            languages: Optional[List[LanguageRequirement]],
            # Standard fields
            department_id: Optional[str],
            employment_type: Optional[EmploymentTypeEnum],
            experience_level: Optional[ExperienceLevelEnum],
            work_location_type: Optional[WorkLocationTypeEnum],
            office_locations: Optional[List[str]],
            remote_restrictions: Optional[str],
            number_of_openings: int,
            requisition_id: Optional[str],
            # Financial fields
            salary_currency: Optional[str],
            salary_min: Optional[Decimal],
            salary_max: Optional[Decimal],
            salary_period: Optional[SalaryPeriodEnum],
            show_salary: bool,
            budget_max: Optional[Decimal],
            approved_budget_max: Optional[Decimal],
            financial_approver_id: Optional[CompanyUserId],
            approved_at: Optional[datetime],
            # Ownership fields
            hiring_manager_id: Optional[CompanyUserId],
            recruiter_id: Optional[CompanyUserId],
            created_by_id: Optional[CompanyUserId],
            # Lifecycle fields
            status: JobPositionStatusEnum,
            closed_reason: Optional[ClosedReasonEnum],
            closed_at: Optional[datetime],
            published_at: Optional[datetime],
            # Custom fields
            custom_fields_config: Optional[List[CustomFieldDefinition]],
            custom_fields_values: Optional[Dict[str, Any]],
            source_workflow_id: Optional[str],
            # Pipeline and screening
            candidate_pipeline_id: Optional[str],
            screening_template_id: Optional[str],
            killer_questions: Optional[List[Dict[str, Any]]],
            # Application configuration
            application_mode: Optional[ApplicationModeEnum],
            required_sections: Optional[List[str]],
            # Visibility and publishing
            visibility: JobPositionVisibilityEnum,
            public_slug: Optional[str],
            open_at: Optional[datetime],
            application_deadline: Optional[date],
            # Timestamps
            created_at: datetime,
            updated_at: datetime,
    ) -> 'JobPosition':
        """Create JobPosition from repository data - only for repositories to use"""
        return cls(
            id=id,
            title=title,
            company_id=company_id,
            # Workflow system - Publication (PO)
            job_position_workflow_id=job_position_workflow_id,
            phase_workflows=phase_workflows or {},
            stage_id=stage_id,
            stage_assignments=stage_assignments or {},
            # Workflow system - Candidate Application (CA)
            candidate_application_workflow_id=candidate_application_workflow_id,
            # Content fields
            description=description,
            job_category=job_category,
            skills=skills or [],
            languages=languages or [],
            # Standard fields
            department_id=department_id,
            employment_type=employment_type,
            experience_level=experience_level,
            work_location_type=work_location_type,
            office_locations=office_locations or [],
            remote_restrictions=remote_restrictions,
            number_of_openings=number_of_openings or 1,
            requisition_id=requisition_id,
            # Financial fields
            salary_currency=salary_currency,
            salary_min=salary_min,
            salary_max=salary_max,
            salary_period=salary_period,
            show_salary=show_salary if show_salary is not None else False,
            budget_max=budget_max,
            approved_budget_max=approved_budget_max,
            financial_approver_id=financial_approver_id,
            approved_at=approved_at,
            # Ownership fields
            hiring_manager_id=hiring_manager_id,
            recruiter_id=recruiter_id,
            created_by_id=created_by_id,
            # Lifecycle fields
            status=status or JobPositionStatusEnum.DRAFT,
            closed_reason=closed_reason,
            closed_at=closed_at,
            published_at=published_at,
            # Custom fields
            custom_fields_config=custom_fields_config or [],
            custom_fields_values=custom_fields_values or {},
            source_workflow_id=source_workflow_id,
            # Pipeline and screening
            candidate_pipeline_id=candidate_pipeline_id,
            screening_template_id=screening_template_id,
            killer_questions=killer_questions or [],
            # Application configuration
            application_mode=application_mode or ApplicationModeEnum.SHORT,
            required_sections=required_sections or [],
            # Visibility and publishing
            visibility=visibility,
            public_slug=public_slug,
            open_at=open_at,
            application_deadline=application_deadline,
            # Timestamps
            created_at=created_at,
            updated_at=updated_at
        )

    # ==================== STATUS TRANSITION METHODS ====================
    # Valid status transitions as a class-level constant
    # Format: {current_status: [allowed_target_statuses]}
    VALID_TRANSITIONS = {
        JobPositionStatusEnum.DRAFT: [
            JobPositionStatusEnum.PENDING_APPROVAL,
            JobPositionStatusEnum.PUBLISHED,  # For 2-stage workflows (quick mode)
            JobPositionStatusEnum.ARCHIVED,
        ],
        JobPositionStatusEnum.PENDING_APPROVAL: [
            JobPositionStatusEnum.APPROVED,
            JobPositionStatusEnum.REJECTED,
            JobPositionStatusEnum.DRAFT,  # Can withdraw approval request
        ],
        JobPositionStatusEnum.APPROVED: [
            JobPositionStatusEnum.PUBLISHED,
            JobPositionStatusEnum.DRAFT,  # Can revert to draft for more edits
        ],
        JobPositionStatusEnum.REJECTED: [
            JobPositionStatusEnum.DRAFT,  # Go back to draft for revisions
        ],
        JobPositionStatusEnum.PUBLISHED: [
            JobPositionStatusEnum.ON_HOLD,
            JobPositionStatusEnum.CLOSED,
            JobPositionStatusEnum.ARCHIVED,
        ],
        JobPositionStatusEnum.ON_HOLD: [
            JobPositionStatusEnum.PUBLISHED,  # Resume
            JobPositionStatusEnum.CLOSED,
            JobPositionStatusEnum.ARCHIVED,
        ],
        JobPositionStatusEnum.CLOSED: [
            JobPositionStatusEnum.ARCHIVED,
            JobPositionStatusEnum.DRAFT,  # Reopen by going back to draft (clone-like behavior)
        ],
        JobPositionStatusEnum.ARCHIVED: [],  # Terminal state - no transitions allowed
    }

    # Fields that are locked (cannot be modified) based on status
    # After approval/publish, financial fields are frozen
    LOCKED_FIELDS_BY_STATUS = {
        JobPositionStatusEnum.APPROVED: ['budget_max'],
        JobPositionStatusEnum.PUBLISHED: ['budget_max', 'custom_fields_config'],
        JobPositionStatusEnum.ON_HOLD: ['budget_max', 'custom_fields_config'],
        JobPositionStatusEnum.CLOSED: ['budget_max', 'custom_fields_config', 'salary_min', 'salary_max'],
        JobPositionStatusEnum.ARCHIVED: ['*'],  # All fields locked
    }

    def can_transition_to(self, target_status: JobPositionStatusEnum) -> bool:
        """Check if transition to target status is valid"""
        allowed = self.VALID_TRANSITIONS.get(self.status, [])
        return target_status in allowed

    def _validate_transition(self, target_status: JobPositionStatusEnum) -> None:
        """Validate that transition to target status is allowed"""
        if not self.can_transition_to(target_status):
            raise JobPositionInvalidStatusTransitionError(
                current_status=self.status.value,
                target_status=target_status.value
            )

    def is_field_locked(self, field_name: str) -> bool:
        """Check if a specific field is locked based on current status"""
        locked_fields = self.LOCKED_FIELDS_BY_STATUS.get(self.status, [])
        return '*' in locked_fields or field_name in locked_fields

    def request_approval(self) -> None:
        """
        Request approval for the job position.
        Transition: DRAFT -> PENDING_APPROVAL
        """
        self._validate_transition(JobPositionStatusEnum.PENDING_APPROVAL)
        self._validate_required_fields_for_approval()
        self.status = JobPositionStatusEnum.PENDING_APPROVAL
        self.updated_at = datetime.utcnow()

    def approve(self, approver_id: CompanyUserId) -> None:
        """
        Approve the job position.
        Transition: PENDING_APPROVAL -> APPROVED
        Also captures budget snapshot if budget_max is set.
        """
        self._validate_transition(JobPositionStatusEnum.APPROVED)

        # Capture budget snapshot on approval
        if self.budget_max is not None:
            self.approved_budget_max = self.budget_max
            self.financial_approver_id = approver_id
            self.approved_at = datetime.utcnow()

        self.status = JobPositionStatusEnum.APPROVED
        self.updated_at = datetime.utcnow()

    def reject(self, reason: Optional[str] = None) -> None:
        """
        Reject the job position approval request.
        Transition: PENDING_APPROVAL -> REJECTED
        """
        self._validate_transition(JobPositionStatusEnum.REJECTED)
        self.status = JobPositionStatusEnum.REJECTED
        self.updated_at = datetime.utcnow()
        # Rejection reason can be stored in a comment or separate field

    def publish(self) -> None:
        """
        Publish the job position to make it visible to candidates.
        Transition: APPROVED -> PUBLISHED or DRAFT -> PUBLISHED (for quick mode)
        """
        # Allow direct publish from DRAFT (for 2-stage workflows) or from APPROVED
        if self.status == JobPositionStatusEnum.DRAFT:
            self._validate_transition(JobPositionStatusEnum.PUBLISHED)
            self._validate_required_fields_for_approval()
        else:
            self._validate_transition(JobPositionStatusEnum.PUBLISHED)

        self.status = JobPositionStatusEnum.PUBLISHED
        self.published_at = datetime.utcnow()
        self.visibility = JobPositionVisibilityEnum.PUBLIC
        self.updated_at = datetime.utcnow()

    def put_on_hold(self) -> None:
        """
        Pause the job position (stop accepting applications).
        Transition: PUBLISHED -> ON_HOLD
        """
        self._validate_transition(JobPositionStatusEnum.ON_HOLD)
        self.status = JobPositionStatusEnum.ON_HOLD
        self.visibility = JobPositionVisibilityEnum.HIDDEN
        self.updated_at = datetime.utcnow()

    def resume(self) -> None:
        """
        Resume a paused job position.
        Transition: ON_HOLD -> PUBLISHED
        """
        self._validate_transition(JobPositionStatusEnum.PUBLISHED)
        self.status = JobPositionStatusEnum.PUBLISHED
        self.visibility = JobPositionVisibilityEnum.PUBLIC
        self.updated_at = datetime.utcnow()

    def close(self, reason: ClosedReasonEnum) -> None:
        """
        Close the job position with a reason.
        Transition: PUBLISHED/ON_HOLD -> CLOSED
        """
        self._validate_transition(JobPositionStatusEnum.CLOSED)
        self.status = JobPositionStatusEnum.CLOSED
        self.closed_reason = reason
        self.closed_at = datetime.utcnow()
        self.visibility = JobPositionVisibilityEnum.HIDDEN
        self.updated_at = datetime.utcnow()

    def archive(self) -> None:
        """
        Archive the job position (soft delete).
        Can be done from DRAFT, PUBLISHED, ON_HOLD, or CLOSED.
        """
        self._validate_transition(JobPositionStatusEnum.ARCHIVED)
        self.status = JobPositionStatusEnum.ARCHIVED
        self.visibility = JobPositionVisibilityEnum.HIDDEN
        self.updated_at = datetime.utcnow()

    def revert_to_draft(self) -> None:
        """
        Return to draft status for revisions.
        Transition: REJECTED/APPROVED/CLOSED -> DRAFT
        """
        self._validate_transition(JobPositionStatusEnum.DRAFT)
        self.status = JobPositionStatusEnum.DRAFT
        self.visibility = JobPositionVisibilityEnum.HIDDEN
        self.updated_at = datetime.utcnow()

    def withdraw_approval_request(self) -> None:
        """
        Withdraw an approval request.
        Transition: PENDING_APPROVAL -> DRAFT
        """
        self._validate_transition(JobPositionStatusEnum.DRAFT)
        self.status = JobPositionStatusEnum.DRAFT
        self.updated_at = datetime.utcnow()

    def set_screening_template(self, template_id: str) -> None:
        """
        Set the screening template for this job position.
        Can only be set in DRAFT or PENDING_APPROVAL status.
        """
        if self.is_field_locked("screening_template_id"):
            from src.company_bc.job_position.domain.exceptions import JobPositionFieldLockedError
            raise JobPositionFieldLockedError(
                "screening_template_id",
                self.status.value,
                "Cannot change screening template in current status"
            )
        self.screening_template_id = template_id
        self.updated_at = datetime.utcnow()

    def clone(self, new_id: JobPositionId) -> 'JobPosition':
        """
        Create a clone of this job position with a new ID.
        The clone starts in DRAFT status with cleared lifecycle fields.
        """
        now = datetime.utcnow()
        return JobPosition(
            id=new_id,
            title=f"{self.title} (Copy)",
            company_id=self.company_id,
            # Workflow system
            job_position_workflow_id=self.job_position_workflow_id,
            phase_workflows=self.phase_workflows.copy() if self.phase_workflows else {},
            stage_id=None,  # Reset stage
            stage_assignments={},  # Reset assignments
            # Content fields
            description=self.description,
            job_category=self.job_category,
            skills=self.skills.copy() if self.skills else [],
            languages=self.languages.copy() if self.languages else [],
            # Standard fields
            department_id=self.department_id,
            employment_type=self.employment_type,
            experience_level=self.experience_level,
            work_location_type=self.work_location_type,
            office_locations=self.office_locations.copy() if self.office_locations else [],
            remote_restrictions=self.remote_restrictions,
            number_of_openings=self.number_of_openings,
            requisition_id=None,  # Clear requisition ID
            # Financial fields
            salary_currency=self.salary_currency,
            salary_min=self.salary_min,
            salary_max=self.salary_max,
            salary_period=self.salary_period,
            show_salary=self.show_salary,
            budget_max=self.budget_max,
            approved_budget_max=None,  # Clear approval
            financial_approver_id=None,
            approved_at=None,
            # Ownership fields - preserve
            hiring_manager_id=self.hiring_manager_id,
            recruiter_id=self.recruiter_id,
            created_by_id=self.created_by_id,
            # Lifecycle - reset to DRAFT
            status=JobPositionStatusEnum.DRAFT,
            closed_reason=None,
            closed_at=None,
            published_at=None,
            # Custom fields - copy config and values
            custom_fields_config=self.custom_fields_config.copy() if self.custom_fields_config else [],
            custom_fields_values=self.custom_fields_values.copy() if self.custom_fields_values else {},
            source_workflow_id=self.source_workflow_id,
            # Pipeline and screening
            candidate_pipeline_id=self.candidate_pipeline_id,
            screening_template_id=self.screening_template_id,
            killer_questions=self.killer_questions.copy() if self.killer_questions else [],
            # Workflow system - Candidate Application (CA)
            candidate_application_workflow_id=self.candidate_application_workflow_id,
            # Application configuration - copy from original
            application_mode=self.application_mode,
            required_sections=self.required_sections.copy() if self.required_sections else [],
            # Visibility - reset
            visibility=JobPositionVisibilityEnum.HIDDEN,
            public_slug=None,  # Need new slug
            open_at=None,
            application_deadline=None,
            # Timestamps
            created_at=now,
            updated_at=now
        )

    def _validate_required_fields_for_approval(self) -> None:
        """Validate that required fields are set before requesting approval"""
        errors = []
        if not self.title or self.title.strip() == "":
            errors.append("Title is required")
        if not self.description or self.description.strip() == "":
            errors.append("Description is required")
        if self.number_of_openings < 1:
            errors.append("Number of openings must be at least 1")

        if errors:
            raise JobPositionValidationError(", ".join(errors))

    def validate_salary_against_budget(self) -> None:
        """
        Validate that salary does not exceed budget limit.
        Used before approval to ensure financial compliance.
        """
        if self.budget_max is not None and self.salary_max is not None:
            if self.salary_max > self.budget_max:
                raise JobPositionBudgetExceededError(
                    salary_max=str(self.salary_max),
                    budget_max=str(self.budget_max)
                )

    def get_allowed_transitions(self) -> List[JobPositionStatusEnum]:
        """Get list of statuses this position can transition to"""
        return self.VALID_TRANSITIONS.get(self.status, [])

    # ==================== CUSTOM FIELDS SNAPSHOT ====================

    def copy_custom_fields_from_workflow(
            self,
            workflow_custom_fields: List[CustomFieldDefinition],
            source_workflow_id: str
    ) -> None:
        """
        Copy custom field definitions from a workflow at creation time.

        This implements the Snapshot Pattern - the field definitions are COPIED
        from the workflow, not referenced. This means:
        1. Changes to the workflow don't affect existing positions
        2. After publish, the structure is frozen
        3. Each position has its own copy of field definitions

        Args:
            workflow_custom_fields: List of custom field definitions from the workflow
            source_workflow_id: The workflow ID this was copied from
        """
        if self.status not in [JobPositionStatusEnum.DRAFT]:
            raise JobPositionFieldLockedError(
                field_name="custom_fields_config",
                current_status=self.status.value,
                message="Custom fields config can only be copied in DRAFT status"
            )

        # Deep copy the definitions
        self.custom_fields_config = [
            CustomFieldDefinition(
                field_key=cf.field_key,
                label=cf.label,
                field_type=cf.field_type,
                options=cf.options.copy() if cf.options else None,
                is_required=cf.is_required,
                candidate_visible=cf.candidate_visible,
                validation_rules=cf.validation_rules.copy() if cf.validation_rules else None,
                sort_order=cf.sort_order,
                is_active=cf.is_active
            )
            for cf in workflow_custom_fields
        ]
        self.source_workflow_id = source_workflow_id
        self.updated_at = datetime.utcnow()

    def freeze_custom_fields(self) -> None:
        """
        Freeze the custom fields structure on publish.
        After this, only field values can be changed, not the structure.
        Called automatically during publish().
        """
        # The freezing is enforced by LOCKED_FIELDS_BY_STATUS
        # This method is here for explicit documentation and potential future logic
        pass

    def update_custom_field_value(self, field_key: str, value: Any) -> None:
        """
        Update a single custom field value.

        Args:
            field_key: The field key to update
            value: The new value

        Raises:
            JobPositionValidationError: If field doesn't exist
            JobPositionFieldLockedError: If all fields are locked (ARCHIVED status)
        """
        if self.is_field_locked('*'):
            raise JobPositionFieldLockedError(
                field_name="custom_fields_values",
                current_status=self.status.value
            )

        # Validate field exists in config
        field_exists = any(
            cf.field_key == field_key
            for cf in self.custom_fields_config
        )
        if not field_exists and self.custom_fields_config:
            raise JobPositionValidationError(
                f"Custom field '{field_key}' is not defined in this position's configuration"
            )

        self.custom_fields_values[field_key] = value
        self.updated_at = datetime.utcnow()

    def get_custom_field_definition(self, field_key: str) -> Optional[CustomFieldDefinition]:
        """Get a custom field definition by key"""
        for cf in self.custom_fields_config:
            if cf.field_key == field_key:
                return cf
        return None

    def toggle_custom_field_active(self, field_key: str, is_active: bool) -> None:
        """
        Toggle whether a custom field is active for this position.
        Recruiters can deactivate fields they don't need for a specific position.

        Args:
            field_key: The field key to toggle
            is_active: Whether the field should be active

        Raises:
            JobPositionValidationError: If field doesn't exist
            JobPositionFieldLockedError: If in PUBLISHED or later status
        """
        if self.is_field_locked('custom_fields_config'):
            raise JobPositionFieldLockedError(
                field_name="custom_fields_config",
                current_status=self.status.value
            )

        for i, cf in enumerate(self.custom_fields_config):
            if cf.field_key == field_key:
                self.custom_fields_config[i] = (
                    cf.activate() if is_active else cf.deactivate()
                )
                self.updated_at = datetime.utcnow()
                return

        raise JobPositionValidationError(
            f"Custom field '{field_key}' not found in this position's configuration"
        )

    # ==================== FINANCIAL CONTROLS ====================

    def set_budget(self, budget_max: Decimal) -> None:
        """
        Set the budget maximum for this position.

        Args:
            budget_max: The maximum budget for this position

        Raises:
            JobPositionFieldLockedError: If budget is locked (after approval)
        """
        if self.is_field_locked('budget_max'):
            raise JobPositionFieldLockedError(
                field_name="budget_max",
                current_status=self.status.value
            )

        self.budget_max = budget_max
        self.updated_at = datetime.utcnow()

    def set_salary_range(
            self,
            salary_min: Optional[Decimal] = None,
            salary_max: Optional[Decimal] = None,
            salary_currency: Optional[str] = None,
            salary_period: Optional[SalaryPeriodEnum] = None
    ) -> None:
        """
        Set the salary range for this position.

        Args:
            salary_min: Minimum salary
            salary_max: Maximum salary
            salary_currency: Currency code (ISO 4217)
            salary_period: Period for salary (yearly, monthly, hourly)

        Raises:
            JobPositionFieldLockedError: If salary is locked (after close)
            JobPositionValidationError: If salary_max < salary_min
        """
        if self.is_field_locked('salary_min') or self.is_field_locked('salary_max'):
            raise JobPositionFieldLockedError(
                field_name="salary_range",
                current_status=self.status.value
            )

        # Validate salary range
        if salary_min is not None and salary_max is not None:
            if salary_max < salary_min:
                raise JobPositionValidationError(
                    "Salary maximum cannot be less than salary minimum"
                )

        if salary_min is not None:
            self.salary_min = salary_min
        if salary_max is not None:
            self.salary_max = salary_max
        if salary_currency is not None:
            self.salary_currency = salary_currency
        if salary_period is not None:
            self.salary_period = salary_period

        self.updated_at = datetime.utcnow()

    def is_within_budget(self, offer_amount: Decimal) -> bool:
        """
        Check if an offer amount is within the approved budget.
        Used when making offers to candidates.

        Args:
            offer_amount: The offer amount to check

        Returns:
            True if within budget (or no budget set), False otherwise
        """
        if self.approved_budget_max is None:
            return True
        return offer_amount <= self.approved_budget_max

    def get_budget_remaining(self) -> Optional[Decimal]:
        """
        Get remaining budget (for tracking multiple offers).
        This is a simple implementation - could be extended with offer tracking.
        """
        return self.approved_budget_max
