from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List

from src.company_candidate.domain.enums import (
    CompanyCandidateStatus,
    OwnershipStatus,
    CandidatePriority,
)
from src.company_candidate.domain.value_objects import (
    CompanyCandidateId,
    VisibilitySettings,
)
from src.company_candidate.domain.exceptions import (
    CompanyCandidateValidationError,
    InvalidOwnershipTransitionError,
)
from src.company.domain.value_objects import CompanyId
from src.company.domain.value_objects.company_user_id import CompanyUserId
from src.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class CompanyCandidate:
    """
    CompanyCandidate domain entity
    Represents the relationship between a company and a candidate
    """
    id: CompanyCandidateId
    company_id: CompanyId
    candidate_id: CandidateId
    status: CompanyCandidateStatus
    ownership_status: OwnershipStatus
    created_by_user_id: CompanyUserId
    workflow_id: Optional[str]  # Will be replaced with WorkflowId value object later
    current_stage_id: Optional[str]  # Will be replaced with StageId value object later
    invited_at: datetime
    confirmed_at: Optional[datetime]
    rejected_at: Optional[datetime]
    archived_at: Optional[datetime]
    visibility_settings: VisibilitySettings
    tags: List[str]
    internal_notes: str
    position: Optional[str]
    department: Optional[str]
    priority: CandidatePriority
    # Resume fields
    lead_id: Optional[str]  # Will be replaced with LeadId value object when Lead entity is created
    source: str  # Origin of candidate: "job_application", "manual_import", "referral", etc.
    resume_url: Optional[str]  # S3 path or URL to uploaded resume
    resume_uploaded_by: Optional[CompanyUserId]  # User who uploaded the resume
    resume_uploaded_at: Optional[datetime]  # When resume was uploaded
    created_at: datetime
    updated_at: datetime

    @classmethod
    def create(
        cls,
        id: CompanyCandidateId,
        company_id: CompanyId,
        candidate_id: CandidateId,
        created_by_user_id: CompanyUserId,
        source: str,
        position: Optional[str] = None,
        department: Optional[str] = None,
        priority: CandidatePriority = CandidatePriority.MEDIUM,
        visibility_settings: Optional[VisibilitySettings] = None,
        tags: Optional[List[str]] = None,
        internal_notes: str = "",
        ownership_status: OwnershipStatus = OwnershipStatus.COMPANY_OWNED,
        lead_id: Optional[str] = None,
        resume_url: Optional[str] = None,
        resume_uploaded_by: Optional[CompanyUserId] = None,
    ) -> "CompanyCandidate":
        """
        Factory method to create a new company-candidate relationship

        Args:
            id: CompanyCandidate ID (required, must be provided from outside)
            company_id: Company ID
            candidate_id: Candidate ID
            created_by_user_id: User who created this relationship
            source: Origin of candidate (e.g., "job_application", "manual_import", "referral")
            position: Position the candidate is being considered for
            department: Department within the company
            priority: Priority level (LOW, MEDIUM, HIGH)
            visibility_settings: What data the company can see
            tags: Internal tags for organization
            internal_notes: Internal notes about the candidate
            ownership_status: Who owns the data (company or user)
            lead_id: Optional Lead ID that originated this candidate
            resume_url: Optional resume file URL/path
            resume_uploaded_by: Optional user who uploaded the resume

        Returns:
            CompanyCandidate: New company-candidate relationship

        Raises:
            CompanyCandidateValidationError: If data is invalid
        """
        # Validations
        if not company_id:
            raise CompanyCandidateValidationError("company_id is required")

        if not candidate_id:
            raise CompanyCandidateValidationError("candidate_id is required")

        if not created_by_user_id:
            raise CompanyCandidateValidationError("created_by_user_id is required")

        if not source:
            raise CompanyCandidateValidationError("source is required")

        # Default values
        now = datetime.utcnow()

        # Default visibility settings
        if visibility_settings is None:
            visibility_settings = VisibilitySettings.default()

        # Default tags
        if tags is None:
            tags = []

        # Determine initial status based on ownership
        if ownership_status == OwnershipStatus.COMPANY_OWNED:
            initial_status = CompanyCandidateStatus.ACTIVE
        else:
            initial_status = CompanyCandidateStatus.PENDING_CONFIRMATION

        # Set resume_uploaded_at if resume_url is provided
        resume_uploaded_at_value = now if resume_url else None

        return cls(
            id=id,
            company_id=company_id,
            candidate_id=candidate_id,
            status=initial_status,
            ownership_status=ownership_status,
            created_by_user_id=created_by_user_id,
            workflow_id=None,
            current_stage_id=None,
            invited_at=now,
            confirmed_at=None,
            rejected_at=None,
            archived_at=None,
            visibility_settings=visibility_settings,
            tags=tags,
            internal_notes=internal_notes,
            position=position,
            department=department,
            priority=priority,
            lead_id=lead_id,
            source=source,
            resume_url=resume_url,
            resume_uploaded_by=resume_uploaded_by,
            resume_uploaded_at=resume_uploaded_at_value,
            created_at=now,
            updated_at=now,
        )

    def update(
        self,
        position: Optional[str],
        department: Optional[str],
        priority: CandidatePriority,
        visibility_settings: VisibilitySettings,
        tags: List[str],
        internal_notes: str,
    ) -> "CompanyCandidate":
        """
        Updates the company-candidate relationship with new values
        Returns a new instance (immutability)

        Args:
            position: New position
            department: New department
            priority: New priority
            visibility_settings: New visibility settings
            tags: New tags
            internal_notes: New internal notes

        Returns:
            CompanyCandidate: New instance with updated data
        """
        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=self.status,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=self.current_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=self.rejected_at,
            archived_at=self.archived_at,
            visibility_settings=visibility_settings,
            tags=tags,
            internal_notes=internal_notes,
            position=position,
            department=department,
            priority=priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def update_resume(
        self,
        resume_url: str,
        uploaded_by: CompanyUserId,
    ) -> "CompanyCandidate":
        """
        Updates the resume for this candidate
        Returns a new instance (immutability)

        Args:
            resume_url: New resume URL/path
            uploaded_by: User who uploaded the resume

        Returns:
            CompanyCandidate: New instance with updated resume
        """
        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=self.status,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=self.current_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=self.rejected_at,
            archived_at=self.archived_at,
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=resume_url,
            resume_uploaded_by=uploaded_by,
            resume_uploaded_at=datetime.utcnow(),
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def confirm(self) -> "CompanyCandidate":
        """
        Confirms the relationship (user accepted the invitation)

        Returns:
            CompanyCandidate: New instance with ACTIVE status

        Raises:
            CompanyCandidateValidationError: If already confirmed or rejected
        """
        if self.status == CompanyCandidateStatus.ACTIVE:
            return self

        if self.status == CompanyCandidateStatus.REJECTED:
            raise CompanyCandidateValidationError(
                "Cannot confirm a rejected relationship"
            )

        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=CompanyCandidateStatus.ACTIVE,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=self.current_stage_id,
            invited_at=self.invited_at,
            confirmed_at=datetime.utcnow(),
            rejected_at=self.rejected_at,
            archived_at=self.archived_at,
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def reject(self) -> "CompanyCandidate":
        """
        Rejects the relationship (user declined the invitation)

        Returns:
            CompanyCandidate: New instance with REJECTED status
        """
        if self.status == CompanyCandidateStatus.REJECTED:
            return self

        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=CompanyCandidateStatus.REJECTED,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=self.current_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=datetime.utcnow(),
            archived_at=self.archived_at,
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def archive(self) -> "CompanyCandidate":
        """
        Archives the relationship

        Returns:
            CompanyCandidate: New instance with ARCHIVED status
        """
        if self.status == CompanyCandidateStatus.ARCHIVED:
            return self

        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=CompanyCandidateStatus.ARCHIVED,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=self.current_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=self.rejected_at,
            archived_at=datetime.utcnow(),
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def transfer_ownership_to_user(self) -> "CompanyCandidate":
        """
        Transfers ownership from company to user
        This happens when a user confirms their profile

        Returns:
            CompanyCandidate: New instance with USER_OWNED status

        Raises:
            InvalidOwnershipTransitionError: If already user-owned
        """
        if self.ownership_status == OwnershipStatus.USER_OWNED:
            raise InvalidOwnershipTransitionError(
                "Ownership is already transferred to user"
            )

        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=self.status,
            ownership_status=OwnershipStatus.USER_OWNED,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=self.current_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=self.rejected_at,
            archived_at=self.archived_at,
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def assign_workflow(self, workflow_id: str, initial_stage_id: str) -> "CompanyCandidate":
        """
        Assigns a workflow and initial stage to this candidate

        Args:
            workflow_id: Workflow ID
            initial_stage_id: Initial stage ID

        Returns:
            CompanyCandidate: New instance with workflow assigned
        """
        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=self.status,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=workflow_id,
            current_stage_id=initial_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=self.rejected_at,
            archived_at=self.archived_at,
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def change_stage(self, new_stage_id: str) -> "CompanyCandidate":
        """
        Moves the candidate to a new stage in the workflow

        Args:
            new_stage_id: New stage ID

        Returns:
            CompanyCandidate: New instance with new stage

        Raises:
            CompanyCandidateValidationError: If no workflow is assigned
        """
        if not self.workflow_id:
            raise CompanyCandidateValidationError(
                "Cannot change stage without an assigned workflow"
            )

        return CompanyCandidate(
            id=self.id,
            company_id=self.company_id,
            candidate_id=self.candidate_id,
            status=self.status,
            ownership_status=self.ownership_status,
            created_by_user_id=self.created_by_user_id,
            workflow_id=self.workflow_id,
            current_stage_id=new_stage_id,
            invited_at=self.invited_at,
            confirmed_at=self.confirmed_at,
            rejected_at=self.rejected_at,
            archived_at=self.archived_at,
            visibility_settings=self.visibility_settings,
            tags=self.tags,
            internal_notes=self.internal_notes,
            position=self.position,
            department=self.department,
            priority=self.priority,
            lead_id=self.lead_id,
            source=self.source,
            resume_url=self.resume_url,
            resume_uploaded_by=self.resume_uploaded_by,
            resume_uploaded_at=self.resume_uploaded_at,
            created_at=self.created_at,
            updated_at=datetime.utcnow(),
        )

    def is_active(self) -> bool:
        """Checks if the relationship is active"""
        return self.status == CompanyCandidateStatus.ACTIVE

    def is_archived(self) -> bool:
        """Checks if the relationship is archived"""
        return self.status == CompanyCandidateStatus.ARCHIVED

    def is_pending(self) -> bool:
        """Checks if the relationship is pending"""
        return self.status in [
            CompanyCandidateStatus.PENDING_INVITATION,
            CompanyCandidateStatus.PENDING_CONFIRMATION,
        ]

    def is_company_owned(self) -> bool:
        """Checks if data is owned by the company"""
        return self.ownership_status == OwnershipStatus.COMPANY_OWNED

    def is_user_owned(self) -> bool:
        """Checks if data is owned by the user"""
        return self.ownership_status == OwnershipStatus.USER_OWNED
