from typing import Optional, List, Any

from src.workflow.domain.entities.workflow_stage import WorkflowStage
from src.workflow.domain.value_objects.workflow_stage_id import WorkflowStageId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.value_objects.stage_style import StageStyle
from src.company_workflow.domain.infrastructure.workflow_stage_repository_interface import WorkflowStageRepositoryInterface
from src.company_workflow.infrastructure.models.workflow_stage_model import WorkflowStageModel
from src.company_workflow.domain.enums.stage_type import StageType
from src.phase.domain.value_objects.phase_id import PhaseId


class WorkflowStageRepository(WorkflowStageRepositoryInterface):
    """Repository implementation for workflow stage operations"""

    def __init__(self, database: Any) -> None:
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

    def get_initial_stage(self, workflow_id: CompanyWorkflowId) -> Optional[WorkflowStage]:
        """Get the initial stage of a workflow"""
        with self._database.get_session() as session:
            model = session.query(WorkflowStageModel).filter_by(
                workflow_id=str(workflow_id),
                stage_type=StageType.INITIAL.value
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def get_final_stages(self, workflow_id: CompanyWorkflowId) -> List[WorkflowStage]:
        """Get all final stages of a workflow (SUCCESS and FAIL stages)"""
        with self._database.get_session() as session:
            models = session.query(WorkflowStageModel).filter(
                WorkflowStageModel.workflow_id == str(workflow_id),
                WorkflowStageModel.stage_type.in_([StageType.SUCCESS.value, StageType.FAIL.value])
            ).all()
            return [self._to_domain(model) for model in models]

    def list_by_phase(self, phase_id: PhaseId) -> List[WorkflowStage]:
        """List all stages for a phase, ordered by order field"""
        with self._database.get_session() as session:
            # First get the workflow for this phase
            from src.company_workflow.infrastructure.models.company_workflow_model import CompanyWorkflowModel
            workflow = session.query(CompanyWorkflowModel).filter_by(phase_id=str(phase_id)).first()
            
            if not workflow:
                return []
            
            # Then get all stages for that workflow
            models = session.query(WorkflowStageModel).filter_by(
                workflow_id=str(workflow.id)
            ).order_by(WorkflowStageModel.order).all()
            return [self._to_domain(model) for model in models]

    def _to_domain(self, model: WorkflowStageModel) -> WorkflowStage:
        """Convert model to domain entity"""
        from decimal import Decimal
        from typing import cast

        # Handle JSON fields that can be lists or None
        default_role_ids = cast(list[str], model.default_role_ids) if model.default_role_ids else []
        default_assigned_users = cast(list[str], model.default_assigned_users) if model.default_assigned_users else []

        return WorkflowStage(
            id=WorkflowStageId.from_string(model.id),
            workflow_id=CompanyWorkflowId.from_string(model.workflow_id),
            name=model.name,
            description=model.description,
            stage_type=StageType(model.stage_type),
            order=model.order,
            allow_skip=model.allow_skip,
            estimated_duration_days=model.estimated_duration_days,
            is_active=model.is_active,
            default_role_ids=default_role_ids,
            default_assigned_users=default_assigned_users,
            email_template_id=model.email_template_id,
            custom_email_text=model.custom_email_text,
            deadline_days=model.deadline_days,
            estimated_cost=Decimal(str(model.estimated_cost)) if model.estimated_cost is not None else None,
            next_phase_id=model.next_phase_id,
            kanban_display=model.kanban_display,
            style=StageStyle.from_dict(model.style) if model.style else StageStyle.create(),
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
            allow_skip=entity.allow_skip,
            estimated_duration_days=entity.estimated_duration_days,
            is_active=entity.is_active,
            default_role_ids=entity.default_role_ids,
            default_assigned_users=entity.default_assigned_users,
            email_template_id=entity.email_template_id,
            custom_email_text=entity.custom_email_text,
            deadline_days=entity.deadline_days,
            estimated_cost=float(entity.estimated_cost) if entity.estimated_cost is not None else None,
            next_phase_id=entity.next_phase_id,
            kanban_display=entity.kanban_display,
            style=entity.style.to_dict(),
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
