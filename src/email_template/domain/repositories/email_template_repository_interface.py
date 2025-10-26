"""
Email Template Repository Interface
Phase 7: Repository interface for email template persistence
"""

from abc import ABC, abstractmethod
from typing import List, Optional

from src.email_template.domain.entities.email_template import EmailTemplate
from src.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.email_template.domain.enums.trigger_event import TriggerEvent


class EmailTemplateRepositoryInterface(ABC):
    """Repository interface for email templates"""

    @abstractmethod
    def save(self, template: EmailTemplate) -> EmailTemplate:
        """
        Save or update an email template

        Args:
            template: EmailTemplate entity to save

        Returns:
            Saved EmailTemplate entity
        """
        pass

    @abstractmethod
    def get_by_id(self, template_id: EmailTemplateId) -> Optional[EmailTemplate]:
        """
        Get email template by ID

        Args:
            template_id: Template ID

        Returns:
            EmailTemplate if found, None otherwise
        """
        pass

    @abstractmethod
    def get_by_key(self, workflow_id: str, template_key: str) -> Optional[EmailTemplate]:
        """
        Get email template by workflow and key

        Args:
            workflow_id: Workflow ID
            template_key: Template key

        Returns:
            EmailTemplate if found, None otherwise
        """
        pass

    @abstractmethod
    def list_by_workflow(self, workflow_id: str, active_only: bool = False) -> List[EmailTemplate]:
        """
        Get all email templates for a workflow

        Args:
            workflow_id: Workflow ID
            active_only: If True, return only active templates

        Returns:
            List of EmailTemplate entities
        """
        pass

    @abstractmethod
    def list_by_stage(self, stage_id: str, active_only: bool = False) -> List[EmailTemplate]:
        """
        Get all email templates for a specific stage

        Args:
            stage_id: Stage ID
            active_only: If True, return only active templates

        Returns:
            List of EmailTemplate entities
        """
        pass

    @abstractmethod
    def list_by_trigger(
        self,
        workflow_id: str,
        trigger_event: TriggerEvent,
        stage_id: Optional[str] = None,
        active_only: bool = True
    ) -> List[EmailTemplate]:
        """
        Get templates by trigger event

        Args:
            workflow_id: Workflow ID
            trigger_event: Trigger event
            stage_id: Optional stage ID filter
            active_only: If True, return only active templates

        Returns:
            List of EmailTemplate entities matching criteria
        """
        pass

    @abstractmethod
    def delete(self, template_id: EmailTemplateId) -> bool:
        """
        Delete an email template

        Args:
            template_id: Template ID

        Returns:
            True if deleted, False if not found
        """
        pass

    @abstractmethod
    def exists(self, workflow_id: str, stage_id: Optional[str], trigger_event: TriggerEvent) -> bool:
        """
        Check if a template already exists for the given criteria

        Args:
            workflow_id: Workflow ID
            stage_id: Stage ID (can be None)
            trigger_event: Trigger event

        Returns:
            True if exists, False otherwise
        """
        pass
