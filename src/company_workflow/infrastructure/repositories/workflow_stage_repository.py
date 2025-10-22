from typing import Optional, List

from src.company_workflow.domain.entities.workflow_stage import WorkflowStage
from src.company_workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
from src.company_workflow.domain.enums.stage_type import StageType
from src.company_workflow.domain.enums.stage_outcome import StageOutcome


class WorkflowStageRepository(WorkflowStageRepositoryInterface):
    """Repository implementation for workflow stage operations"""

    def __init__(self, database):
        self._database = database

    def save(self, stage: WorkflowStage) -> None:
        """Save a workflow stage"""
        model = self._to_model(stage)
        with self._database.get_session() as session:
            existing = session.query(WorkflowStageModel).filter_by(id=str(stage.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, stage_id: WorkflowStageId) -> Optional[WorkflowStage]:
        """Get stage by ID"""
        with self._database.get_session() as session:
            model = session.query(WorkflowStageModel).filter_by(id=str(stage_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_workflow(self, workflow_id: CompanyWorkflowId) -> List[WorkflowStage]:
        """List all stages for a workflow, ordered by order field"""
        with self._database.get_session() as session:
            models = session.query(WorkflowStageModel).filter_by(
                workflow_id=str(workflow_id)
            ).order_by(WorkflowStageModel.order).all()
            return [self._to_domain(model) for model in models]

    def delete(self, stage_id: WorkflowStageId) -> None:
        """Delete a stage"""
        with self._database.get_session() as session:
            session.query(WorkflowStageModel).filter_by(id=str(stage_id)).delete()
            session.commit()

    def _to_domain(self, model: WorkflowStageModel) -> WorkflowStage:
        """Convert model to domain entity"""
        return WorkflowStage(
            id=WorkflowStageId.from_string(model.id),
            workflow_id=CompanyWorkflowId.from_string(model.workflow_id),
            name=model.name,
            description=model.description,
            stage_type=StageType(model.stage_type),
            order=model.order,
            required_outcome=StageOutcome(model.required_outcome) if model.required_outcome else None,
            estimated_duration_days=model.estimated_duration_days,
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: WorkflowStage) -> WorkflowStageModel:
        """Convert domain entity to model"""
        return WorkflowStageModel(
            id=str(entity.id),
            workflow_id=str(entity.workflow_id),
            name=entity.name,
            description=entity.description,
            stage_type=entity.stage_type.value,
            order=entity.order,
            required_outcome=entity.required_outcome.value if entity.required_outcome else None,
            estimated_duration_days=entity.estimated_duration_days,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
