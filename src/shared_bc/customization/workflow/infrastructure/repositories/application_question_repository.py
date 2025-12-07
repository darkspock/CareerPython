from typing import Optional, List, Any

from src.company_bc.company.domain.value_objects import CompanyId
from src.shared_bc.customization.workflow.domain.entities.application_question import (
    ApplicationQuestion
)
from src.shared_bc.customization.workflow.domain.enums.application_question_field_type import (
    ApplicationQuestionFieldType
)
from src.shared_bc.customization.workflow.domain.interfaces.application_question_repository_interface import (
    ApplicationQuestionRepositoryInterface
)
from src.shared_bc.customization.workflow.domain.value_objects.application_question_id import (
    ApplicationQuestionId
)
from src.shared_bc.customization.workflow.domain.value_objects.workflow_id import WorkflowId
from src.shared_bc.customization.workflow.infrastructure.models.application_question_model import (
    ApplicationQuestionModel
)


class ApplicationQuestionRepository(ApplicationQuestionRepositoryInterface):
    """Repository implementation for ApplicationQuestion entity."""

    def __init__(self, database: Any) -> None:
        self._database = database

    def get_by_id(self, question_id: ApplicationQuestionId) -> Optional[ApplicationQuestion]:
        """Get an application question by ID."""
        with self._database.get_session() as session:
            model = session.query(ApplicationQuestionModel).filter_by(
                id=str(question_id)
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def list_by_workflow(
        self,
        workflow_id: WorkflowId,
        active_only: bool = True
    ) -> List[ApplicationQuestion]:
        """List all application questions for a workflow."""
        with self._database.get_session() as session:
            query = session.query(ApplicationQuestionModel).filter_by(
                workflow_id=str(workflow_id)
            )
            if active_only:
                query = query.filter_by(is_active=True)
            models = query.order_by(ApplicationQuestionModel.sort_order).all()
            return [self._to_domain(model) for model in models]

    def get_by_field_key(
        self,
        workflow_id: WorkflowId,
        field_key: str
    ) -> Optional[ApplicationQuestion]:
        """Get an application question by field key within a workflow."""
        with self._database.get_session() as session:
            model = session.query(ApplicationQuestionModel).filter_by(
                workflow_id=str(workflow_id),
                field_key=field_key
            ).first()
            if model:
                return self._to_domain(model)
            return None

    def save(self, question: ApplicationQuestion) -> None:
        """Save an application question (insert or update)."""
        model = self._to_model(question)
        with self._database.get_session() as session:
            existing = session.query(ApplicationQuestionModel).filter_by(
                id=str(question.id)
            ).first()
            if existing:
                session.merge(model)
            else:
                session.add(model)
            session.commit()

    def delete(self, question_id: ApplicationQuestionId) -> None:
        """Delete an application question."""
        with self._database.get_session() as session:
            session.query(ApplicationQuestionModel).filter_by(
                id=str(question_id)
            ).delete()
            session.commit()

    def _to_domain(self, model: ApplicationQuestionModel) -> ApplicationQuestion:
        """Convert model to domain entity."""
        return ApplicationQuestion(
            id=ApplicationQuestionId.from_string(str(model.id)),
            workflow_id=WorkflowId.from_string(str(model.workflow_id)),
            company_id=CompanyId.from_string(str(model.company_id)),
            field_key=str(model.field_key),
            label=str(model.label),
            description=model.description,
            field_type=ApplicationQuestionFieldType(str(model.field_type)),
            options=model.options,
            is_required_default=bool(model.is_required_default),
            validation_rules=model.validation_rules,
            sort_order=int(model.sort_order),
            is_active=bool(model.is_active),
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _to_model(self, entity: ApplicationQuestion) -> ApplicationQuestionModel:
        """Convert domain entity to model."""
        return ApplicationQuestionModel(
            id=str(entity.id.value),
            workflow_id=str(entity.workflow_id.value),
            company_id=str(entity.company_id.value),
            field_key=entity.field_key,
            label=entity.label,
            description=entity.description,
            field_type=entity.field_type.value,
            options=entity.options,
            is_required_default=entity.is_required_default,
            validation_rules=entity.validation_rules,
            sort_order=entity.sort_order,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
