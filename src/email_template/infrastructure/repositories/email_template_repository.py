"""
Email Template Repository Implementation
Phase 7: SQLAlchemy implementation of email template repository
"""

from typing import List, Optional

from core.database import DatabaseInterface
from src.email_template.domain.entities.email_template import EmailTemplate
from src.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.email_template.domain.enums.trigger_event import TriggerEvent
from src.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.email_template.infrastructure.models.email_template_model import EmailTemplateModel


class EmailTemplateRepository(EmailTemplateRepositoryInterface):
    """SQLAlchemy implementation of EmailTemplateRepositoryInterface"""

    def __init__(self, database: DatabaseInterface):
        self.database = database

    def save(self, template: EmailTemplate) -> EmailTemplate:
        """Save or update an email template"""
        with self.database.get_session() as session:
            model = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.id == template.id.value
            ).first()

            if model:
                # Update existing
                self._update_model_from_entity(model, template)
            else:
                # Create new
                model = self._create_model_from_entity(template)
                session.add(model)

            session.commit()
            session.refresh(model)

            return self._create_entity_from_model(model)

    def get_by_id(self, template_id: EmailTemplateId) -> Optional[EmailTemplate]:
        """Get email template by ID"""
        with self.database.get_session() as session:
            model = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.id == template_id.value
            ).first()

            if not model:
                return None

            return self._create_entity_from_model(model)

    def get_by_key(self, workflow_id: str, template_key: str) -> Optional[EmailTemplate]:
        """Get email template by workflow and key"""
        with self.database.get_session() as session:
            model = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.workflow_id == workflow_id,
                EmailTemplateModel.template_key == template_key
            ).first()

            if not model:
                return None

            return self._create_entity_from_model(model)

    def list_by_workflow(self, workflow_id: str, active_only: bool = False) -> List[EmailTemplate]:
        """Get all email templates for a workflow"""
        with self.database.get_session() as session:
            query = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.workflow_id == workflow_id
            )

            if active_only:
                query = query.filter(EmailTemplateModel.is_active == True)

            models = query.order_by(EmailTemplateModel.created_at.desc()).all()

            return [self._create_entity_from_model(model) for model in models]

    def list_by_stage(self, stage_id: str, active_only: bool = False) -> List[EmailTemplate]:
        """Get all email templates for a specific stage"""
        with self.database.get_session() as session:
            query = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.stage_id == stage_id
            )

            if active_only:
                query = query.filter(EmailTemplateModel.is_active == True)

            models = query.order_by(EmailTemplateModel.created_at.desc()).all()

            return [self._create_entity_from_model(model) for model in models]

    def list_by_trigger(
        self,
        workflow_id: str,
        trigger_event: TriggerEvent,
        stage_id: Optional[str] = None,
        active_only: bool = True
    ) -> List[EmailTemplate]:
        """Get templates by trigger event"""
        with self.database.get_session() as session:
            query = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.workflow_id == workflow_id,
                EmailTemplateModel.trigger_event == trigger_event.value
            )

            if stage_id is not None:
                query = query.filter(EmailTemplateModel.stage_id == stage_id)

            if active_only:
                query = query.filter(EmailTemplateModel.is_active == True)

            models = query.all()

            return [self._create_entity_from_model(model) for model in models]

    def delete(self, template_id: EmailTemplateId) -> bool:
        """Delete an email template"""
        with self.database.get_session() as session:
            model = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.id == template_id.value
            ).first()

            if not model:
                return False

            session.delete(model)
            session.commit()
            return True

    def exists(self, workflow_id: str, stage_id: Optional[str], trigger_event: TriggerEvent) -> bool:
        """Check if a template already exists for the given criteria"""
        with self.database.get_session() as session:
            query = session.query(EmailTemplateModel).filter(
                EmailTemplateModel.workflow_id == workflow_id,
                EmailTemplateModel.trigger_event == trigger_event.value
            )

            if stage_id is not None:
                query = query.filter(EmailTemplateModel.stage_id == stage_id)
            else:
                query = query.filter(EmailTemplateModel.stage_id.is_(None))

            return query.first() is not None

    def _create_entity_from_model(self, model: EmailTemplateModel) -> EmailTemplate:
        """Convert SQLAlchemy model to domain entity"""
        return EmailTemplate._from_repository(
            id=EmailTemplateId.from_string(model.id),
            workflow_id=model.workflow_id,
            stage_id=model.stage_id,
            template_name=model.template_name,
            template_key=model.template_key,
            subject=model.subject,
            body_html=model.body_html,
            body_text=model.body_text,
            available_variables=model.available_variables,
            trigger_event=TriggerEvent(model.trigger_event),
            is_active=model.is_active,
            created_at=model.created_at,
            updated_at=model.updated_at
        )

    def _create_model_from_entity(self, template: EmailTemplate) -> EmailTemplateModel:
        """Convert domain entity to SQLAlchemy model"""
        return EmailTemplateModel(
            id=template.id.value,
            workflow_id=template.workflow_id,
            stage_id=template.stage_id,
            template_name=template.template_name,
            template_key=template.template_key,
            subject=template.subject,
            body_html=template.body_html,
            body_text=template.body_text,
            available_variables=template.available_variables,
            trigger_event=template.trigger_event.value,
            is_active=template.is_active,
            created_at=template.created_at,
            updated_at=template.updated_at
        )

    def _update_model_from_entity(self, model: EmailTemplateModel, template: EmailTemplate) -> None:
        """Update SQLAlchemy model with data from domain entity"""
        model.workflow_id = template.workflow_id
        model.stage_id = template.stage_id
        model.template_name = template.template_name
        model.template_key = template.template_key
        model.subject = template.subject
        model.body_html = template.body_html
        model.body_text = template.body_text
        model.available_variables = template.available_variables
        model.trigger_event = template.trigger_event.value
        model.is_active = template.is_active
        model.updated_at = template.updated_at
