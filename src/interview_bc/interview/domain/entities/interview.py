from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import Optional, List

from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.interview_bc.interview.domain.enums.interview_enums import (
    InterviewStatusEnum,
    InterviewTypeEnum,
    InterviewModeEnum,
    InterviewProcessTypeEnum
)
from src.interview_bc.interview.domain.value_objects.interview_id import InterviewId
from src.interview_bc.interview_template.domain.value_objects.interview_template_id import InterviewTemplateId
from src.company_bc.job_position.domain.value_objects.job_position_id import JobPositionId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_bc.company_role.domain.value_objects.company_role_id import CompanyRoleId


@dataclass
class Interview:
    """Interview domain entity"""
    id: InterviewId
    candidate_id: CandidateId
    required_roles: List[CompanyRoleId]  # Obligatory: List of CompanyRole IDs required for this interview
    created_at: datetime
    updated_at: datetime
    job_position_id: Optional[JobPositionId] = None
    application_id: Optional[CandidateApplicationId] = None
    interview_template_id: Optional[InterviewTemplateId] = None
    workflow_stage_id: Optional[WorkflowStageId] = None  # Stage where this interview is conducted
    process_type: Optional[InterviewProcessTypeEnum] = None  # Moment in the selection process
    interview_type: InterviewTypeEnum = InterviewTypeEnum.CUSTOM
    interview_mode: Optional[InterviewModeEnum] = None  # Mode: AUTOMATIC, AI, MANUAL
    status: InterviewStatusEnum = InterviewStatusEnum.ENABLED
    title: Optional[str] = None
    description: Optional[str] = None
    scheduled_at: Optional[datetime] = None
    deadline_date: Optional[datetime] = None  # Optional deadline date
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_minutes: Optional[int] = None
    interviewers: List[str] = field(default_factory=list)  # List of interviewers name
    interviewer_notes: Optional[str] = None
    candidate_notes: Optional[str] = None
    score: Optional[float] = None  # Overall interview score (0-100)
    feedback: Optional[str] = None
    free_answers: Optional[str] = None  # Free text answers from candidate
    link_token: Optional[str] = None  # Unique token for secure interview link access
    link_expires_at: Optional[datetime] = None  # Expiration date for the interview link

    def start(self, started_by: Optional[str] = None) -> None:
        """Start the interview"""
        if self.status != InterviewStatusEnum.ENABLED:
            raise ValueError("Can only start interviews that are in ENABLED status")

        self.status = InterviewStatusEnum.IN_PROGRESS
        self.started_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        if started_by:
            self.updated_by = started_by

    def finish(self, finished_by: Optional[str] = None) -> None:
        """Finish the interview"""
        if self.status != InterviewStatusEnum.IN_PROGRESS:
            raise ValueError("Can only finish interviews that are IN_PROGRESS")

        self.status = InterviewStatusEnum.FINISHED
        self.finished_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # Calculate duration if started
        if self.started_at:
            duration = self.finished_at - self.started_at
            self.duration_minutes = int(duration.total_seconds() / 60)

        if finished_by:
            self.updated_by = finished_by

    def pause(self, paused_by: Optional[str] = None) -> None:
        """Pause the interview"""
        if self.status != InterviewStatusEnum.IN_PROGRESS:
            raise ValueError("Can only pause interviews that are IN_PROGRESS")

        self.status = InterviewStatusEnum.PAUSED
        self.updated_at = datetime.utcnow()
        if paused_by:
            self.updated_by = paused_by

    def resume(self, resumed_by: Optional[str] = None) -> None:
        """Resume a paused interview"""
        if self.status != InterviewStatusEnum.PAUSED:
            raise ValueError("Can only resume interviews that are PAUSED")

        self.status = InterviewStatusEnum.IN_PROGRESS
        self.updated_at = datetime.utcnow()
        if resumed_by:
            self.updated_by = resumed_by

    def discard(self, discarded_by: Optional[str] = None) -> None:
        """Discard the interview"""
        if self.status == InterviewStatusEnum.DISCARDED:
            return

        self.status = InterviewStatusEnum.DISCARDED
        self.updated_at = datetime.utcnow()
        if discarded_by:
            self.updated_by = discarded_by

    def schedule(self, scheduled_at: datetime, scheduled_by: Optional[str] = None) -> None:
        """Schedule the interview"""
        if scheduled_at <= datetime.utcnow():
            raise ValueError("Cannot schedule interview in the past")

        self.scheduled_at = scheduled_at
        self.updated_at = datetime.utcnow()
        if scheduled_by:
            self.updated_by = scheduled_by

    def update_scheduled_at(self, scheduled_at: datetime, updated_by: Optional[str] = None, allow_past: bool = False) -> None:
        """Update scheduled_at date, optionally allowing past dates (for editing existing interviews)"""
        if allow_past:
            # When allow_past=True, allow any date (for editing existing interviews)
            # This allows keeping past dates or updating other fields without date validation
            self.scheduled_at = scheduled_at
        else:
            # When allow_past=False, validate that we're not scheduling in the past
            if scheduled_at <= datetime.utcnow():
                # Prevent scheduling new interviews in the past
                if self.scheduled_at is None:
                    raise ValueError("Cannot schedule interview in the past")
                # Prevent moving to an earlier past date
                elif self.scheduled_at and scheduled_at < self.scheduled_at:
                    raise ValueError("Cannot reschedule interview to an earlier past date")
            self.scheduled_at = scheduled_at
        
        self.updated_at = datetime.utcnow()
        if updated_by:
            self.updated_by = updated_by

    def set_deadline(self, deadline_date: datetime, set_by: Optional[str] = None) -> None:
        """Set the deadline date for the interview"""
        if deadline_date <= datetime.utcnow():
            raise ValueError("Cannot set deadline in the past")
        
        if self.scheduled_at and deadline_date < self.scheduled_at:
            raise ValueError("Deadline cannot be before scheduled date")

        self.deadline_date = deadline_date
        self.updated_at = datetime.utcnow()
        if set_by:
            self.updated_by = set_by

    def set_score(self, score: float, scored_by: Optional[str] = None) -> None:
        """Set the interview score"""
        if score < 0 or score > 100:
            raise ValueError("Score must be between 0 and 100")

        self.score = score
        self.updated_at = datetime.utcnow()
        if scored_by:
            self.updated_by = scored_by

    def add_interviewer_notes(self, notes: str, added_by: Optional[str] = None) -> None:
        """Add interviewer notes"""
        self.interviewer_notes = notes
        self.updated_at = datetime.utcnow()
        if added_by:
            self.updated_by = added_by

    def add_feedback(self, feedback: str, added_by: Optional[str] = None) -> None:
        """Add interview feedback"""
        self.feedback = feedback
        self.updated_at = datetime.utcnow()
        if added_by:
            self.updated_by = added_by

    def update_details(
            self,
            title: Optional[str] = None,
            description: Optional[str] = None,
            process_type: Optional[InterviewProcessTypeEnum] = None,
            interview_type: Optional[InterviewTypeEnum] = None,
            interview_mode: Optional[InterviewModeEnum] = None,
            job_position_id: Optional[JobPositionId] = None,
            application_id: Optional[CandidateApplicationId] = None,
            interview_template_id: Optional[InterviewTemplateId] = None,
            workflow_stage_id: Optional[WorkflowStageId] = None,
            deadline_date: Optional[datetime] = None,
            updated_by: Optional[str] = None
    ) -> None:
        """Update interview details"""
        if title is not None:
            self.title = title
        if description is not None:
            self.description = description
        if process_type is not None:
            self.process_type = process_type
        if interview_type is not None:
            self.interview_type = interview_type
        if interview_mode is not None:
            self.interview_mode = interview_mode
        if job_position_id is not None:
            self.job_position_id = job_position_id
        if application_id is not None:
            self.application_id = application_id
        if interview_template_id is not None:
            self.interview_template_id = interview_template_id
        if workflow_stage_id is not None:
            self.workflow_stage_id = workflow_stage_id
        if deadline_date is not None:
            if deadline_date <= datetime.utcnow():
                raise ValueError("Cannot set deadline in the past")
            if self.scheduled_at and deadline_date < self.scheduled_at:
                raise ValueError("Deadline cannot be before scheduled date")
            self.deadline_date = deadline_date

        self.updated_at = datetime.utcnow()
        if updated_by:
            self.updated_by = updated_by

    def update_required_roles(self, required_roles: List[CompanyRoleId], updated_by: Optional[str] = None) -> None:
        """Update the required roles for this interview"""
        if not required_roles:
            raise ValueError("Required roles cannot be empty")
        
        self.required_roles = required_roles
        self.updated_at = datetime.utcnow()
        if updated_by:
            self.updated_by = updated_by

    def is_scheduled(self) -> bool:
        """Check if interview is scheduled"""
        return self.scheduled_at is not None

    def is_in_progress(self) -> bool:
        """Check if interview is in progress"""
        return self.status == InterviewStatusEnum.IN_PROGRESS

    def is_finished(self) -> bool:
        """Check if interview is finished"""
        return self.status == InterviewStatusEnum.FINISHED

    def is_paused(self) -> bool:
        """Check if interview is paused"""
        return self.status == InterviewStatusEnum.PAUSED

    def is_discarded(self) -> bool:
        """Check if interview is discarded"""
        return self.status == InterviewStatusEnum.DISCARDED

    def get_duration_minutes(self) -> Optional[int]:
        """Get interview duration in minutes"""
        if self.duration_minutes:
            return self.duration_minutes

        if self.started_at and self.finished_at:
            duration = self.finished_at - self.started_at
            return int(duration.total_seconds() / 60)

        return None

    def generate_link_token(self, expires_in_days: int = 30) -> None:
        """Generate a unique token for secure interview link access"""
        import secrets
        self.link_token = secrets.token_urlsafe(32)  # 32 bytes = 43 characters base64
        self.link_expires_at = datetime.utcnow() + timedelta(days=expires_in_days)
        self.updated_at = datetime.utcnow()

    def get_shareable_link(self, base_url: str) -> Optional[str]:
        """Get the shareable link for this interview"""
        if not self.link_token:
            return None
        return f"{base_url}/interviews/{self.id.value}/access?token={self.link_token}"

    def is_link_valid(self) -> bool:
        """Check if the interview link is still valid"""
        if not self.link_token:
            return False
        if self.link_expires_at and self.link_expires_at < datetime.utcnow():
            return False
        return True

    @staticmethod
    def create(
            id: InterviewId,
            candidate_id: CandidateId,
            required_roles: List[CompanyRoleId],
            process_type: Optional[InterviewProcessTypeEnum] = None,
            interview_type: InterviewTypeEnum = InterviewTypeEnum.CUSTOM,
            interview_mode: Optional[InterviewModeEnum] = None,
            job_position_id: Optional[JobPositionId] = None,
            application_id: Optional[CandidateApplicationId] = None,
            interview_template_id: Optional[InterviewTemplateId] = None,
            workflow_stage_id: Optional[WorkflowStageId] = None,
            title: Optional[str] = None,
            description: Optional[str] = None,
            scheduled_at: Optional[datetime] = None,
            deadline_date: Optional[datetime] = None,
            created_by: Optional[str] = None
    ) -> 'Interview':
        """Create a new interview
        
        Args:
            id: Interview ID
            candidate_id: Candidate ID (obligatory)
            required_roles: List of CompanyRole IDs required for this interview (obligatory)
            process_type: Moment in the selection process (optional)
            interview_type: Type of interview (default: CUSTOM)
            interview_mode: Execution mode (optional)
            job_position_id: Job position ID (optional)
            application_id: Application ID (optional)
            interview_template_id: Template ID (optional)
            workflow_stage_id: Workflow stage ID (optional)
            title: Interview title (optional)
            description: Interview description (optional)
            scheduled_at: Scheduled date and time (optional)
            deadline_date: Deadline date (optional)
            created_by: User ID who created the interview (optional)
            
        Raises:
            ValueError: If required_roles is empty
        """
        if not required_roles:
            raise ValueError("Required roles cannot be empty")
        
        if deadline_date and scheduled_at and deadline_date < scheduled_at:
            raise ValueError("Deadline cannot be before scheduled date")
        
        now = datetime.utcnow()
        return Interview(
            id=id,
            candidate_id=candidate_id,
            required_roles=required_roles,
            process_type=process_type,
            job_position_id=job_position_id,
            application_id=application_id,
            interview_template_id=interview_template_id,
            workflow_stage_id=workflow_stage_id,
            interview_type=interview_type,
            interview_mode=interview_mode,
            status=InterviewStatusEnum.ENABLED,
            title=title,
            description=description,
            scheduled_at=scheduled_at,
            deadline_date=deadline_date,
            created_at=now,
            updated_at=now,
        )
