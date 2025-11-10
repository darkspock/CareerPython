"""
Email Template Controller for managing email templates
Phase 7: Email Integration System
"""
import logging
from typing import List, Optional

from fastapi import HTTPException

from src.notification_bc.email_template.application.commands.activate_email_template_command import ActivateEmailTemplateCommand
from src.notification_bc.email_template.application.commands.create_email_template_command import CreateEmailTemplateCommand
from src.notification_bc.email_template.application.commands.deactivate_email_template_command import DeactivateEmailTemplateCommand
from src.notification_bc.email_template.application.commands.delete_email_template_command import DeleteEmailTemplateCommand
from src.notification_bc.email_template.application.commands.update_email_template_command import UpdateEmailTemplateCommand
from src.notification_bc.email_template.application.dtos.email_template_dto import EmailTemplateDto
from src.notification_bc.email_template.application.queries.get_email_template_by_id_query import GetEmailTemplateByIdQuery
from src.notification_bc.email_template.application.queries.get_email_templates_by_trigger_query import GetEmailTemplatesByTriggerQuery
from src.notification_bc.email_template.application.queries.list_email_templates_by_stage_query import ListEmailTemplatesByStageQuery
from src.notification_bc.email_template.application.queries.list_email_templates_by_workflow_query import \
    ListEmailTemplatesByWorkflowQuery
from src.notification_bc.email_template.domain import TriggerEvent
from src.framework.application.command_bus import CommandBus
from src.framework.application.query_bus import QueryBus

logger = logging.getLogger(__name__)


class EmailTemplateController:
    """Controller for managing email templates"""

    def __init__(
            self,
            command_bus: CommandBus,
            query_bus: QueryBus
    ):
        self._command_bus = command_bus
        self._query_bus = query_bus

    def create_template(
            self,
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
    ) -> dict:
        """Create a new email template

        Args:
            workflow_id: ID of the workflow this template belongs to
            template_name: Name of the template
            template_key: Unique key for the template
            subject: Email subject line
            body_html: HTML body of the email
            trigger_event: Event that triggers this email
            available_variables: List of variables that can be used in the template
            stage_id: Optional stage ID if template is stage-specific
            body_text: Optional plain text version of the email
            is_active: Whether the template is active

        Returns:
            Success message with template ID
        """
        try:
            command = CreateEmailTemplateCommand(
                workflow_id=workflow_id,
                template_name=template_name,
                template_key=template_key,
                subject=subject,
                body_html=body_html,
                trigger_event=trigger_event,
                available_variables=available_variables,
                stage_id=stage_id,
                body_text=body_text,
                is_active=is_active
            )

            self._command_bus.execute(command)

            return {
                "message": "Email template created successfully",
                "workflow_id": workflow_id,
                "template_key": template_key
            }

        except ValueError as e:
            logger.warning(f"Invalid create template request: {str(e)}")
            raise HTTPException(status_code=400, detail=str(e))
        except Exception as e:
            logger.error(f"Error creating email template: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error creating email template: {str(e)}")

    def update_template(
            self,
            template_id: str,
            template_name: str,
            subject: str,
            body_html: str,
            available_variables: List[str],
            body_text: Optional[str] = None
    ) -> dict:
        """Update an existing email template

        Args:
            template_id: ID of the template to update
            template_name: Updated template name
            subject: Updated subject line
            body_html: Updated HTML body
            available_variables: Updated list of available variables
            body_text: Updated plain text body

        Returns:
            Success message
        """
        try:
            command = UpdateEmailTemplateCommand(
                template_id=template_id,
                template_name=template_name,
                subject=subject,
                body_html=body_html,
                available_variables=available_variables,
                body_text=body_text
            )

            self._command_bus.execute(command)

            return {
                "message": "Email template updated successfully",
                "template_id": template_id
            }

        except ValueError as e:
            logger.warning(f"Invalid update template request: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error updating email template {template_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error updating email template: {str(e)}")

    def delete_template(self, template_id: str) -> dict:
        """Delete an email template

        Args:
            template_id: ID of the template to delete

        Returns:
            Success message
        """
        try:
            command = DeleteEmailTemplateCommand(template_id=template_id)
            self._command_bus.execute(command)

            return {
                "message": "Email template deleted successfully",
                "template_id": template_id
            }

        except ValueError as e:
            logger.warning(f"Invalid delete template request: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error deleting email template {template_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deleting email template: {str(e)}")

    def activate_template(self, template_id: str) -> dict:
        """Activate an email template

        Args:
            template_id: ID of the template to activate

        Returns:
            Success message
        """
        try:
            command = ActivateEmailTemplateCommand(template_id=template_id)
            self._command_bus.execute(command)

            return {
                "message": "Email template activated successfully",
                "template_id": template_id
            }

        except ValueError as e:
            logger.warning(f"Invalid activate template request: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error activating email template {template_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error activating email template: {str(e)}")

    def deactivate_template(self, template_id: str) -> dict:
        """Deactivate an email template

        Args:
            template_id: ID of the template to deactivate

        Returns:
            Success message
        """
        try:
            command = DeactivateEmailTemplateCommand(template_id=template_id)
            self._command_bus.execute(command)

            return {
                "message": "Email template deactivated successfully",
                "template_id": template_id
            }

        except ValueError as e:
            logger.warning(f"Invalid deactivate template request: {str(e)}")
            raise HTTPException(status_code=404, detail=str(e))
        except Exception as e:
            logger.error(f"Error deactivating email template {template_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error deactivating email template: {str(e)}")

    def get_template_by_id(self, template_id: str) -> Optional[EmailTemplateDto]:
        """Get an email template by ID

        Args:
            template_id: ID of the template to retrieve

        Returns:
            EmailTemplateDto if found, raises 404 if not found
        """
        try:
            query = GetEmailTemplateByIdQuery(template_id=template_id)
            template: Optional[EmailTemplateDto] = self._query_bus.query(query)

            if not template:
                raise HTTPException(status_code=404, detail=f"Email template not found: {template_id}")

            return template

        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting email template {template_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error retrieving email template: {str(e)}")

    def list_templates_by_workflow(
            self,
            workflow_id: str,
            active_only: bool = False
    ) -> List[EmailTemplateDto]:
        """List all email templates for a workflow

        Args:
            workflow_id: ID of the workflow
            active_only: If True, return only active templates

        Returns:
            List of EmailTemplateDto
        """
        try:
            query = ListEmailTemplatesByWorkflowQuery(
                workflow_id=workflow_id,
                active_only=active_only
            )

            templates: List[EmailTemplateDto] = self._query_bus.query(query)
            return templates

        except Exception as e:
            logger.error(f"Error listing templates for workflow {workflow_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error listing templates: {str(e)}")

    def list_templates_by_stage(
            self,
            stage_id: str,
            active_only: bool = False
    ) -> List[EmailTemplateDto]:
        """List all email templates for a stage

        Args:
            stage_id: ID of the stage
            active_only: If True, return only active templates

        Returns:
            List of EmailTemplateDto
        """
        try:
            query = ListEmailTemplatesByStageQuery(
                stage_id=stage_id,
                active_only=active_only
            )

            templates: List[EmailTemplateDto] = self._query_bus.query(query)
            return templates

        except Exception as e:
            logger.error(f"Error listing templates for stage {stage_id}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error listing templates: {str(e)}")

    def get_templates_by_trigger(
            self,
            workflow_id: str,
            trigger_event: TriggerEvent,
            stage_id: Optional[str] = None,
            active_only: bool = True
    ) -> List[EmailTemplateDto]:
        """Get templates by trigger event

        Args:
            workflow_id: ID of the workflow
            trigger_event: Trigger event to filter by
            stage_id: Optional stage ID filter
            active_only: If True, return only active templates

        Returns:
            List of EmailTemplateDto matching the criteria
        """
        try:
            query = GetEmailTemplatesByTriggerQuery(
                workflow_id=workflow_id,
                trigger_event=trigger_event,
                stage_id=stage_id,
                active_only=active_only
            )

            templates: List[EmailTemplateDto] = self._query_bus.query(query)
            return templates

        except Exception as e:
            logger.error(f"Error getting templates by trigger {trigger_event}: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Error getting templates: {str(e)}")
