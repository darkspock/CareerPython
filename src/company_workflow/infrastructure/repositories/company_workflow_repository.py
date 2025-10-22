from typing import Optional, List

from src.company_workflow.domain.entities.company_workflow import CompanyWorkflow
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company.domain.value_objects.company_id import CompanyId
from src.company_workflow.domain.infrastructure.company_workflow_repository_interface import CompanyWorkflowRepositoryInterface
from src.company_workflow.infrastructure.models.company_workflow_model import CompanyWorkflowModel
from src.company_workflow.domain.enums.workflow_status import WorkflowStatus


class CompanyWorkflowRepository(CompanyWorkflowRepositoryInterface):
    """Repository implementation for company workflow operations"""

    def __init__(self, database):
        self._database = database

    def save(self, workflow: CompanyWorkflow) -> None:
        """Save a workflow"""
        model = self._to_model(workflow)
        with self._database.get_session() as session:
            existing = session.query(CompanyWorkflowModel).filter_by(id=str(workflow.id)).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, workflow_id: CompanyWorkflowId) -> Optional[CompanyWorkflow]:
        """Get workflow by ID"""
        with self._database.get_session() as session:
            model = session.query(CompanyWorkflowModel).filter_by(id=str(workflow_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_company(self, company_id: CompanyId) -> List[CompanyWorkflow]:
        """List all workflows for a company"""
        with self._database.get_session() as session:
            models = session.query(CompanyWorkflowModel).filter_by(company_id=str(company_id)).all()
            return [self._to_domain(model) for model in models]

    def get_default_by_company(self, company_id: CompanyId) -> Optional[CompanyWorkflow]:
        """Get the default workflow for a company"""
        with self._database.get_session() as session:
            model = session.query(CompanyWorkflowModel).filter_by(
                company_id=str(company_id),
                is_default=True
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def delete(self, workflow_id: CompanyWorkflowId) -> None:
        """Delete a workflow"""
        with self._database.get_session() as session:
            session.query(CompanyWorkflowModel).filter_by(id=str(workflow_id)).delete()
            session.commit()

    def _to_domain(self, model: CompanyWorkflowModel) -> CompanyWorkflow:
        """Convert model to domain entity"""
        return CompanyWorkflow(
            id=CompanyWorkflowId.from_string(model.id),
            company_id=CompanyId.from_string(model.company_id),
            name=model.name,
            description=model.description,
            status=WorkflowStatus(model.status),
            is_default=model.is_default,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: CompanyWorkflow) -> CompanyWorkflowModel:
        """Convert domain entity to model"""
        return CompanyWorkflowModel(
            id=str(entity.id),
            company_id=str(entity.company_id),
            name=entity.name,
            description=entity.description,
            status=entity.status.value,
            is_default=entity.is_default,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
