"""
Email Template DTO
Phase 7: Data Transfer Object for email templates
"""

from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional

from src.email_template.domain.entities.email_template import EmailTemplate
from src.email_template.domain.enums.trigger_event import TriggerEvent


@dataclass(frozen=True)
class EmailTemplateDto:
    """DTO for email template data"""
    id: str
    workflow_id: str
    stage_id: Optional[str]
    template_name: str
    template_key: str
    subject: str
    body_html: str
    body_text: Optional[str]
    available_variables: List[str]
    trigger_event: TriggerEvent
    is_active: bool
    created_at: datetime
    updated_at: datetime

    @staticmethod
    def from_entity(entity: EmailTemplate) -> 'EmailTemplateDto':
        """Create DTO from domain entity"""
        return EmailTemplateDto(
            id=entity.id.value,
            workflow_id=entity.workflow_id,
            stage_id=entity.stage_id,
            template_name=entity.template_name,
            template_key=entity.template_key,
            subject=entity.subject,
            body_html=entity.body_html,
            body_text=entity.body_text,
            available_variables=entity.available_variables,
            trigger_event=entity.trigger_event,
            is_active=entity.is_active,
            created_at=entity.created_at,
            updated_at=entity.updated_at
        )
