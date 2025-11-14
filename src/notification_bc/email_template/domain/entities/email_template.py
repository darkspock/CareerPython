"""
Email Template Entity
Phase 7: Domain entity for email templates with variable substitution
"""

import re
from dataclasses import dataclass
from datetime import datetime
from typing import List, Optional, Dict, Any

from src.notification_bc.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.notification_bc.email_template.domain.enums.trigger_event import TriggerEvent


@dataclass
class EmailTemplate:
    """
    Email template entity for workflow stage notifications

    Templates use Jinja2-style variables: {{ variable_name }}
    Available variables depend on trigger event context
    """

    id: EmailTemplateId
    workflow_id: str
    stage_id: Optional[str]  # None = applies to all stages
    template_name: str
    template_key: str  # Unique identifier for the template
    subject: str
    body_html: str
    body_text: Optional[str]
    available_variables: List[str]
    trigger_event: TriggerEvent
    is_active: bool
    created_at: datetime
    updated_at: datetime

    def activate(self) -> None:
        """Activate the template"""
        self.is_active = True
        self.updated_at = datetime.utcnow()

    def deactivate(self) -> None:
        """Deactivate the template"""
        self.is_active = False
        self.updated_at = datetime.utcnow()

    def update_content(
        self,
        template_name: str,
        subject: str,
        body_html: str,
        body_text: Optional[str] = None
    ) -> None:
        """Update template content"""
        self.template_name = template_name
        self.subject = subject
        self.body_html = body_html
        self.body_text = body_text
        self.updated_at = datetime.utcnow()

    def render_subject(self, context: Dict[str, Any]) -> str:
        """
        Render subject with variable substitution

        Args:
            context: Dictionary with variable values

        Returns:
            Rendered subject with variables replaced
        """
        return self._render_template(self.subject, context)

    def render_body_html(self, context: Dict[str, Any]) -> str:
        """
        Render HTML body with variable substitution

        Args:
            context: Dictionary with variable values

        Returns:
            Rendered HTML body with variables replaced
        """
        return self._render_template(self.body_html, context)

    def render_body_text(self, context: Dict[str, Any]) -> Optional[str]:
        """
        Render text body with variable substitution

        Args:
            context: Dictionary with variable values

        Returns:
            Rendered text body with variables replaced, or None if no text body
        """
        if not self.body_text:
            return None
        return self._render_template(self.body_text, context)

    def get_missing_variables(self, context: Dict[str, Any]) -> List[str]:
        """
        Get list of variables used in template but missing from context

        Args:
            context: Dictionary with variable values

        Returns:
            List of missing variable names
        """
        used_variables = self.get_used_variables()
        return [var for var in used_variables if var not in context]

    def get_used_variables(self) -> List[str]:
        """
        Extract all variables used in subject and body

        Returns:
            List of unique variable names used in the template
        """
        pattern = r'\{\{\s*(\w+)\s*\}\}'

        variables = set()

        # Extract from subject
        variables.update(re.findall(pattern, self.subject))

        # Extract from HTML body
        variables.update(re.findall(pattern, self.body_html))

        # Extract from text body if exists
        if self.body_text:
            variables.update(re.findall(pattern, self.body_text))

        return sorted(list(variables))

    def validate_variables(self) -> bool:
        """
        Validate that all used variables are in available_variables list

        Returns:
            True if all used variables are available, False otherwise
        """
        used_vars = set(self.get_used_variables())
        available_vars = set(self.available_variables)
        return used_vars.issubset(available_vars)

    def _render_template(self, template: str, context: Dict[str, Any]) -> str:
        """
        Simple template rendering with {{ variable }} substitution

        Args:
            template: Template string with {{ variable }} placeholders
            context: Dictionary with variable values

        Returns:
            Rendered string with variables replaced
        """
        result = template

        # Replace all {{ variable }} with values from context
        for key, value in context.items():
            placeholder = f"{{{{ {key} }}}}"
            placeholder_no_spaces = f"{{{{{key}}}}}"

            # Handle both with and without spaces
            result = result.replace(placeholder, str(value))
            result = result.replace(placeholder_no_spaces, str(value))

        return result

    @staticmethod
    def create(
        workflow_id: str,
        template_name: str,
        template_key: str,
        subject: str,
        body_html: str,
        trigger_event: TriggerEvent,
        available_variables: List[str],
        stage_id: Optional[str] = None,
        body_text: Optional[str] = None,
        is_active: bool = True
    ) -> 'EmailTemplate':
        """
        Factory method to create a new email template

        Args:
            workflow_id: ID of the workflow this template belongs to
            template_name: Human-readable name
            template_key: Unique key for the template
            subject: Email subject (can contain variables)
            body_html: HTML email body (can contain variables)
            trigger_event: Event that triggers this email
            available_variables: List of available variables for substitution
            stage_id: Optional stage ID (None = all stages)
            body_text: Optional plain text body
            is_active: Whether template is active

        Returns:
            New EmailTemplate instance

        Raises:
            ValueError: If validation fails
        """
        # Validations
        if not workflow_id:
            raise ValueError("workflow_id is required")
        if not template_name or len(template_name) > 200:
            raise ValueError("template_name must be 1-200 characters")
        if not template_key or len(template_key) > 100:
            raise ValueError("template_key must be 1-100 characters")
        if not subject or len(subject) > 500:
            raise ValueError("subject must be 1-500 characters")
        if not body_html:
            raise ValueError("body_html is required")
        if not available_variables:
            raise ValueError("available_variables list cannot be empty")

        now = datetime.utcnow()

        return EmailTemplate(
            id=EmailTemplateId.generate(),
            workflow_id=workflow_id,
            stage_id=stage_id,
            template_name=template_name,
            template_key=template_key,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            available_variables=available_variables,
            trigger_event=trigger_event,
            is_active=is_active,
            created_at=now,
            updated_at=now
        )

    @staticmethod
    def _from_repository(
        id: EmailTemplateId,
        workflow_id: str,
        stage_id: Optional[str],
        template_name: str,
        template_key: str,
        subject: str,
        body_html: str,
        body_text: Optional[str],
        available_variables: List[str],
        trigger_event: TriggerEvent,
        is_active: bool,
        created_at: datetime,
        updated_at: datetime
    ) -> 'EmailTemplate':
        """
        Factory method for repository to reconstruct entity from database

        This method is only for repository use - not for business logic
        """
        return EmailTemplate(
            id=id,
            workflow_id=workflow_id,
            stage_id=stage_id,
            template_name=template_name,
            template_key=template_key,
            subject=subject,
            body_html=body_html,
            body_text=body_text,
            available_variables=available_variables,
            trigger_event=trigger_event,
            is_active=is_active,
            created_at=created_at,
            updated_at=updated_at
        )
