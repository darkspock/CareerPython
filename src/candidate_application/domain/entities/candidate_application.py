from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Optional

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.candidate_application.domain.enums.task_status import TaskStatus
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.candidate_application.domain.value_objects.task_priority import TaskPriority
from src.job_position.domain.value_objects.job_position_id import JobPositionId


@dataclass
class CandidateApplication:
    """Entidad del dominio para aplicaciones de candidatos a posiciones"""
    id: CandidateApplicationId
    candidate_id: CandidateId
    job_position_id: JobPositionId
    application_status: ApplicationStatusEnum
    applied_at: datetime
    updated_at: Optional[datetime] = None
    notes: Optional[str] = None
    # Workflow stage tracking fields (Phase 5)
    current_stage_id: Optional[str] = None
    stage_entered_at: Optional[datetime] = None
    stage_deadline: Optional[datetime] = None
    task_status: TaskStatus = TaskStatus.PENDING

    def approve(self) -> None:
        """Aprobar la aplicación"""
        self.application_status = ApplicationStatusEnum.ACCEPTED
        self.updated_at = datetime.utcnow()

    def reject(self, notes: Optional[str] = None) -> None:
        """Rechazar la aplicación"""
        self.application_status = ApplicationStatusEnum.REJECTED
        self.updated_at = datetime.utcnow()
        if notes:
            self.notes = notes

    def start_review(self) -> None:
        """Iniciar revisión de la aplicación"""
        self.application_status = ApplicationStatusEnum.REVIEWING
        self.updated_at = datetime.utcnow()

    def mark_interviewed(self) -> None:
        """Marcar como entrevistado"""
        self.application_status = ApplicationStatusEnum.INTERVIEWED
        self.updated_at = datetime.utcnow()

    def withdraw(self) -> None:
        """Retirar la aplicación"""
        self.application_status = ApplicationStatusEnum.WITHDRAWN
        self.updated_at = datetime.utcnow()

    def update_notes(self, notes: str) -> None:
        """Actualizar notas de la aplicación"""
        self.notes = notes
        self.updated_at = datetime.utcnow()

    def move_to_stage(self, new_stage_id: str, time_limit_hours: Optional[int] = None, changed_by: Optional[str] = None) -> None:
        """Move application to a new workflow stage

        Args:
            new_stage_id: ID of the new stage
            time_limit_hours: Optional time limit for the stage in hours
            changed_by: Optional user ID who moved the application
        """
        self.current_stage_id = new_stage_id
        self.stage_entered_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()

        # Calculate deadline if time limit is provided
        if time_limit_hours is not None and time_limit_hours > 0:
            self.stage_deadline = self.stage_entered_at + timedelta(hours=time_limit_hours)
        else:
            self.stage_deadline = None

        # Reset task status when moving to new stage
        self.task_status = TaskStatus.PENDING

    def calculate_stage_deadline(self, time_limit_hours: Optional[int]) -> Optional[datetime]:
        """Calculate deadline based on stage entry time and time limit

        Args:
            time_limit_hours: Time limit in hours for the stage

        Returns:
            Deadline datetime or None if no time limit or not in a stage
        """
        if self.stage_entered_at is None or time_limit_hours is None or time_limit_hours <= 0:
            return None

        return self.stage_entered_at + timedelta(hours=time_limit_hours)

    def update_task_status(self, status: TaskStatus) -> None:
        """Update the task status for the current stage"""
        self.task_status = status
        self.updated_at = datetime.utcnow()

    def is_stage_deadline_passed(self) -> bool:
        """Check if the current stage deadline has passed"""
        if self.stage_deadline is None:
            return False
        return datetime.utcnow() > self.stage_deadline

    def calculate_priority(self, current_time: Optional[datetime] = None) -> TaskPriority:
        """Calculate task priority for this application

        Phase 6: Task Management
        Priority is based on deadline proximity and time in current stage

        Args:
            current_time: Current time (defaults to now)

        Returns:
            TaskPriority value object with calculated score
        """
        return TaskPriority.calculate(
            stage_deadline=self.stage_deadline,
            stage_entered_at=self.stage_entered_at,
            current_time=current_time
        )

    @staticmethod
    def create(
            id: CandidateApplicationId,
            candidate_id: CandidateId,
            job_position_id: JobPositionId,
            notes: Optional[str] = None,
            initial_stage_id: Optional[str] = None,
            stage_time_limit_hours: Optional[int] = None
    ) -> 'CandidateApplication':
        """Factory method para crear una nueva aplicación

        Args:
            id: Application ID
            candidate_id: Candidate ID
            job_position_id: Job Position ID
            notes: Optional notes
            initial_stage_id: Optional ID of initial workflow stage
            stage_time_limit_hours: Optional time limit for initial stage in hours
        """
        now = datetime.utcnow()

        # Calculate deadline if initial stage has time limit
        stage_deadline = None
        if initial_stage_id and stage_time_limit_hours and stage_time_limit_hours > 0:
            stage_deadline = now + timedelta(hours=stage_time_limit_hours)

        return CandidateApplication(
            id=id,
            candidate_id=candidate_id,
            job_position_id=job_position_id,
            application_status=ApplicationStatusEnum.APPLIED,
            applied_at=now,
            updated_at=now,  # Set updated_at to creation time
            notes=notes,
            # Workflow stage fields
            current_stage_id=initial_stage_id,
            stage_entered_at=now if initial_stage_id else None,
            stage_deadline=stage_deadline,
            task_status=TaskStatus.PENDING
        )
