"""CandidateStage entity - tracks phase progression history for candidate applications"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, Dict, Any
from decimal import Decimal

from src.candidate_application.domain.entities.candidate_application import CandidateApplication
from src.candidate_application_stage.domain.value_objects.candidate_application_stage_id import CandidateApplicationStageId
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.phase.domain.value_objects.phase_id import PhaseId
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


@dataclass
class CandidateApplicationStage:
    """Entity tracking a candidate's progression through a phase/workflow/stage

    This entity captures the history of a candidate's journey through different
    phases, workflows, and stages of the recruitment process. It records when
    they entered and exited each stage, costs, deadlines, and additional data.
    """
    id: CandidateApplicationStageId
    candidate_application_id: CandidateApplicationId
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
        id: CandidateApplicationStageId,
        candidate_application_id: CandidateApplicationId,
        phase_id: Optional[PhaseId] = None,
        workflow_id: Optional[WorkflowId] = None,
        stage_id: Optional[WorkflowStageId] = None,
        started_at: Optional[datetime] = None,
        deadline: Optional[datetime] = None,
        estimated_cost: Optional[Decimal] = None,
        comments: Optional[str] = None,
        data: Optional[Dict[str, Any]] = None
    ) -> 'CandidateApplicationStage':
        """Factory method to create a new candidate stage record"""
        now = datetime.utcnow()
        return CandidateApplicationStage(
            id=id,
            candidate_application_id=candidate_application_id,
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
    ) -> 'CandidateApplicationStage':
        """Mark this stage as completed"""
        return CandidateApplicationStage(
            id=self.id,
            candidate_application_id=self.candidate_application_id,
            phase_id=self.phase_id,
            workflow_id=self.workflow_id,
            stage_id=self.stage_id,
            started_at=self.started_at,
            completed_at=completed_at or datetime.utcnow(),
            deadline=self.deadline,
            estimated_cost=self.estimated_cost,
            actual_cost=actual_cost or self.actual_cost,
            comments=comments or self.comments,
            data=self.data,
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def update_data(self, data: Dict[str, Any]) -> 'CandidateApplicationStage':
        """Update the custom data field"""
        return CandidateApplicationStage(
            id=self.id,
            candidate_application_id=self.candidate_application_id,
            phase_id=self.phase_id,
            workflow_id=self.workflow_id,
            stage_id=self.stage_id,
            started_at=self.started_at,
            completed_at=self.completed_at,
            deadline=self.deadline,
            estimated_cost=self.estimated_cost,
            actual_cost=self.actual_cost,
            comments=self.comments,
            data={**(self.data or {}), **data},
            created_at=self.created_at,
            updated_at=datetime.utcnow()
        )

    def is_completed(self) -> bool:
        """Check if this stage has been completed"""
        return self.completed_at is not None

    def is_overdue(self) -> bool:
        """Check if this stage is overdue (has deadline and not completed)"""
        if self.deadline is None or self.completed_at is not None:
            return False
        return datetime.utcnow() > self.deadline
