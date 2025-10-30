from typing import Optional, Dict, Any

from src.company_workflow.domain.entities.custom_field_value import CustomFieldValue
from src.company_workflow.domain.value_objects.custom_field_value_id import CustomFieldValueId
from src.company_candidate.domain.value_objects.company_candidate_id import CompanyCandidateId
from src.company_workflow.domain.value_objects.company_workflow_id import CompanyWorkflowId
from src.company_workflow.domain.infrastructure.custom_field_value_repository_interface import CustomFieldValueRepositoryInterface
from src.company_workflow.infrastructure.models.custom_field_value_model import CustomFieldValueModel


class CustomFieldValueRepository(CustomFieldValueRepositoryInterface):
    """Repository implementation for custom field value operations"""

    def __init__(self, database: Any) -> None:
        self._database = database

    def save(self, custom_field_value: CustomFieldValue) -> None:
        """Save a custom field value"""
        model = self._to_model(custom_field_value)
        with self._database.get_session() as session:
            existing = session.query(CustomFieldValueModel).filter_by(id=str(custom_field_value.id)).first()
            if existing:
                # Update existing
                existing.company_candidate_id = model.company_candidate_id
                existing.workflow_id = model.workflow_id
                existing.values = model.values
                existing.updated_at = model.updated_at
            else:
                session.add(model)
            session.commit()

    def get_by_id(self, custom_field_value_id: CustomFieldValueId) -> Optional[CustomFieldValue]:
        """Get custom field value by ID"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldValueModel).filter_by(id=str(custom_field_value_id)).first()
            if model:
                return self._to_domain(model)
            return None

    def get_by_company_candidate_and_workflow(
        self, 
        company_candidate_id: CompanyCandidateId, 
        workflow_id: CompanyWorkflowId
    ) -> Optional[CustomFieldValue]:
        """Get custom field value by company candidate and workflow"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldValueModel).filter_by(
                company_candidate_id=str(company_candidate_id),
                workflow_id=str(workflow_id)
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def get_values_by_company_candidate(
        self, 
        company_candidate_id: CompanyCandidateId
    ) -> Dict[str, Dict[str, Any]]:
        """
        Get all custom field values for a company candidate
        Returns a dict keyed by workflow_id, each containing a dict of field_key -> value
        """
        with self._database.get_session() as session:
            models = session.query(CustomFieldValueModel).filter_by(
                company_candidate_id=str(company_candidate_id)
            ).all()
            
            result = {}
            for model in models:
                result[model.workflow_id] = model.values or {}
            return result

    def delete(self, custom_field_value_id: CustomFieldValueId) -> None:
        """Delete a custom field value"""
        with self._database.get_session() as session:
            model = session.query(CustomFieldValueModel).filter_by(id=str(custom_field_value_id)).first()
            if model:
                session.delete(model)
                session.commit()

    def _to_domain(self, model: CustomFieldValueModel) -> CustomFieldValue:
        """Convert model to domain entity"""
        return CustomFieldValue(
            id=CustomFieldValueId(model.id),
            company_candidate_id=CompanyCandidateId(model.company_candidate_id),
            workflow_id=CompanyWorkflowId(model.workflow_id),
            values=model.values or {},
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: CustomFieldValue) -> CustomFieldValueModel:
        """Convert domain entity to model"""
        return CustomFieldValueModel(
            id=str(entity.id),
            company_candidate_id=str(entity.company_candidate_id),
            workflow_id=str(entity.workflow_id),
            values=entity.values,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
