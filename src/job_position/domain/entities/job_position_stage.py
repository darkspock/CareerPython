"""JobPositionStage entity - tracks phase progression history for job positions"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

from src.job_position.domain.value_objects.job_position_stage_id import JobPositionStageId
from src.job_position.domain.value_objects.job_position_id import JobPositionId
from src.phase.domain.value_objects.phase_id import PhaseId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass
class JobPositionStage:
    """Entity tracking a job position's progression through a phase/workflow/stage

    This entity captures the history of a job position's journey through different
    phases, workflows, and stages of the approval/publication process. It records when
    the position entered and exited each stage, costs, deadlines, and additional data.
    """
    id: JobPositionStageId
    job_position_id: JobPositionId
    phase_id: Optional[PhaseId]
    workflow_id: Optional[WorkflowId]
    stage_id: Optional[WorkflowStageId]
    started_at: datetime
    completed_at: Optional[datetime]
    deadline: Optional[datetime]
    estimated_cost: Optional[Decimal]
    actual_cost: Optional[Decimal]
    comments: Optional[str]
    data: Optional[Dict[str, Any]]
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def create(
        id: JobPositionStageId,
        job_position_id: JobPositionId,
        phase_id: Optional[PhaseId] = None,
        workflow_id: Optional[WorkflowId] = None,
        stage_id: Optional[WorkflowStageId] = None,
        started_at: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        estimated_cost: Optional[Decimal] = None,
        comments: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> 'JobPositionStage':
        """Factory method to create a new job position stage record"""
        now = datetime.utcnow()
        return JobPositionStage(
            id=id,
            job_position_id=job_position_id,
            phase_id=phase_id,
            workflow_id=workflow_id,
            stage_id=stage_id,
            started_at=started_at or now,
            completed_at=None,
            deadline=deadline,
            estimated_cost=estimated_cost,
            actual_cost=None,
            comments=comments,
            data=data or {},
            created_at=now,
            updated_at=now
        )

    def complete(
        self,
        completed_at: Optional[datetime] = None,
        actual_cost: Optional[Decimal] = None,
        comments: Optional[str] = None
    ) -> None:
        """Mark this stage as completed (mutates the instance)"""
        self.completed_at = completed_at or datetime.utcnow()
        if actual_cost is not None:
            self.actual_cost = actual_cost
        if comments is not None:
            self.comments = comments
        self.updated_at = datetime.utcnow()

    def update_data(self, data: Dict[str, Any]) -> None:
        """Update the custom data field (mutates the instance)"""
        if self.data is None:
            self.data = {}
        self.data.update(data)
        self.updated_at = datetime.utcnow()

    def is_completed(self) -> bool:
        """Check if this stage has been completed"""
        return self.completed_at is not None

    def is_overdue(self) -> bool:
        """Check if this stage is overdue (has deadline and not completed)"""
        if self.deadline is None or self.completed_at is not None:
            return False
        return datetime.utcnow() > self.deadline

