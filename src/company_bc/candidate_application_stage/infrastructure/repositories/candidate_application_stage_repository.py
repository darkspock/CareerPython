"""CandidateStage repository implementation"""
from typing import List, Optional

from sqlalchemy.orm import Session

from src.company_bc.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.company_bc.candidate_application_stage.domain.entities.candidate_application_stage import \
    CandidateApplicationStage
from src.company_bc.candidate_application_stage.domain.infrastructure.candidate_application_stage_repository_interface import \
    CandidateStageRepositoryInterface
from src.company_bc.candidate_application_stage.domain.value_objects.candidate_application_stage_id import \
    CandidateApplicationStageId
from src.company_bc.candidate_application_stage.infrastructure.models.candidate_stage_model import \
    CandidateApplicationStageModel
from src.shared_bc.customization.phase.domain.value_objects.phase_id import PhaseId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId


class CandidateApplicationStageRepository(CandidateStageRepositoryInterface):
    """SQLAlchemy implementation of CandidateStageRepository"""

    def __init__(self, session: Session):
        self.session = session

    def save(self, candidate_stage: CandidateApplicationStage) -> None:
        """Save a candidate stage"""
        model = self.session.query(CandidateApplicationStageModel).filter_by(id=candidate_stage.id.value).first()

        if model:
            # Update existing
            model.candidate_application_id = candidate_stage.candidate_application_id.value
            model.phase_id = candidate_stage.phase_id.value if candidate_stage.phase_id else None
            model.workflow_id = candidate_stage.workflow_id.value if candidate_stage.workflow_id else None
            model.stage_id = candidate_stage.stage_id.value if candidate_stage.stage_id else None
            model.started_at = candidate_stage.started_at
            model.completed_at = candidate_stage.completed_at
            model.deadline = candidate_stage.deadline
            model.estimated_cost = candidate_stage.estimated_cost
            model.actual_cost = candidate_stage.actual_cost
            model.comments = candidate_stage.comments
            model.data = candidate_stage.data
            model.updated_at = candidate_stage.updated_at
        else:
            # Create new
            model = CandidateApplicationStageModel(
                id=candidate_stage.id.value,
                candidate_application_id=candidate_stage.candidate_application_id.value,
                phase_id=candidate_stage.phase_id.value if candidate_stage.phase_id else None,
                workflow_id=candidate_stage.workflow_id.value if candidate_stage.workflow_id else None,
                stage_id=candidate_stage.stage_id.value if candidate_stage.stage_id else None,
                started_at=candidate_stage.started_at,
                completed_at=candidate_stage.completed_at,
                deadline=candidate_stage.deadline,
                estimated_cost=candidate_stage.estimated_cost,
                actual_cost=candidate_stage.actual_cost,
                comments=candidate_stage.comments,
                data=candidate_stage.data,
                created_at=candidate_stage.created_at,
                updated_at=candidate_stage.updated_at
            )
            self.session.add(model)

        self.session.commit()

    def get_by_id(self, id: CandidateApplicationStageId) -> Optional[CandidateApplicationStage]:
        """Get candidate stage by ID"""
        model = self.session.query(CandidateApplicationStageModel).filter_by(id=id.value).first()
        return self._to_domain(model) if model else None

    def list_by_candidate_application(
            self,
            candidate_application_id: CandidateApplicationId
    ) -> List[CandidateApplicationStage]:
        """Get all stages for a candidate application, ordered by started_at"""
        models = (
            self.session.query(CandidateApplicationStageModel)
            .filter_by(candidate_application_id=candidate_application_id.value)
            .order_by(CandidateApplicationStageModel.started_at.asc())
            .all()
        )
        return [self._to_domain(model) for model in models]

    def list_by_phase(self, phase_id: PhaseId) -> List[CandidateApplicationStage]:
        """Get all stages for a specific phase"""
        models = (
            self.session.query(CandidateApplicationStageModel)
            .filter_by(phase_id=phase_id.value)
            .order_by(CandidateApplicationStageModel.started_at.desc())
            .all()
        )
        return [self._to_domain(model) for model in models]

    def get_current_stage(
            self,
            candidate_application_id: CandidateApplicationId
    ) -> Optional[CandidateApplicationStage]:
        """Get the current (most recent uncompleted) stage for a candidate application"""
        model = (
            self.session.query(CandidateApplicationStageModel)
            .filter_by(
                candidate_application_id=candidate_application_id.value,
                completed_at=None
            )
            .order_by(CandidateApplicationStageModel.started_at.desc())
            .first()
        )
        return self._to_domain(model) if model else None

    def delete(self, id: CandidateApplicationStageId) -> None:
        """Delete a candidate stage"""
        self.session.query(CandidateApplicationStageModel).filter_by(id=id.value).delete()
        self.session.commit()

    def _to_domain(self, model: CandidateApplicationStageModel) -> CandidateApplicationStage:
        """Convert model to domain entity"""
        return CandidateApplicationStage(
            id=CandidateApplicationStageId.from_string(model.id),
            candidate_application_id=CandidateApplicationId.from_string(model.candidate_application_id),
            phase_id=PhaseId.from_string(model.phase_id) if model.phase_id else None,
            workflow_id=WorkflowId.from_string(model.workflow_id) if model.workflow_id else None,
            stage_id=WorkflowStageId.from_string(model.stage_id) if model.stage_id else None,
            started_at=model.started_at,
            completed_at=model.completed_at,
            deadline=model.deadline,
            estimated_cost=model.estimated_cost,
            actual_cost=model.actual_cost,
            comments=model.comments,
            data=model.data,
            created_at=model.created_at,
            updated_at=model.updated_at
        )
