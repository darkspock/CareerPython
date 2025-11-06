from typing import Optional, List, Any

from src.workflow.domain.entities.workflow import Workflow
from src.workflow.domain.value_objects.workflow_id import WorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.workflow.infrastructure.models.workflow_model import WorkflowModel
from src.workflow.domain.enums.workflow_status_enum import WorkflowStatusEnum


class WorkflowRepository(WorkflowRepositoryInterface):
    """Repository implementation for company workflow operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, workflow: Workflow) -> None:
        """Save a workflow"""
        model = self._to_model(workflow)
        with self._database.get_session() as session:
            existing = session.query(WorkflowModel).filter_by(id=str(workflow.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, workflow_id: WorkflowId) -> Optional[Workflow]:
        """Get workflow by ID"""
        with self._database.get_session() as session:
            model = session.query(WorkflowModel).filter_by(id=str(workflow_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_company(self, company_id: CompanyId) -> List[Workflow]:
        """List all workflows for a company"""
        with self._database.get_session() as session:
            models = session.query(WorkflowModel).filter_by(company_id=str(company_id)).all()
            return [self._to_domain(model) for model in models]

    def get_default_by_company(self, company_id: CompanyId) -> Optional[Workflow]:
        """Get the default workflow for a company"""
        with self._database.get_session() as session:
            model = session.query(WorkflowModel).filter_by(
                company_id=str(company_id),
                is_default=True
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def delete(self, workflow_id: WorkflowId) -> None:
        """Delete a workflow"""
        with self._database.get_session() as session:
            session.query(WorkflowModel).filter_by(id=str(workflow_id)).delete()
            session.commit()

    def list_by_phase_id(self, phase_id: str) -> List[Workflow]:
        """List all workflows for a phase - Phase 12"""
        with self._database.get_session() as session:
            models = session.query(WorkflowModel).filter_by(
                phase_id=phase_id,
                status=WorkflowStatusEnum.ACTIVE.value
            ).all()
            return [self._to_domain(model) for model in models]

    def _to_domain(self, model: WorkflowModel) -> Workflow:
        """Convert model to domain entity"""
        return Workflow(
            id=WorkflowId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            phase_id=model.phase_id,
            name=model.name,
            description=model.description,
            status=WorkflowStatusEnum(model.status),
            is_default=model.is_default,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: Workflow) -> WorkflowModel:
        """Convert domain entity to model"""
        return WorkflowModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            phase_id=entity.phase_id,
            name=entity.name,
            description=entity.description,
            status=entity.status.value,
            is_default=entity.is_default,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
