"""
Send Stage Transition Email Handler
Phase 7: Event handler that sends emails when application stage changes
"""

import logging
from typing import Dict, Any

from core.event import EventHandler
from src.candidate_application.domain.events.application_stage_changed_event import ApplicationStageChangedEvent
from src.email_template.domain.enums.trigger_event import TriggerEvent
from src.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.notification.application.commands.send_email_command import SendEmailCommand
from src.shared.application.command_bus import CommandBus

logger = logging.getLogger(__name__)


class SendStageTransitionEmailHandler(EventHandler[ApplicationStageChangedEvent]):
    """Handler that sends emails when application stage changes"""

    def __init__(
            self,
            email_template_repository: EmailTemplateRepositoryInterface,
            command_bus: CommandBus
    ):
        self._email_template_repository = email_template_repository
        self._command_bus = command_bus

    def handle(self, event: ApplicationStageChangedEvent) -> None:
        """
        Handle application stage changed event by sending appropriate emails

        Looks for active email templates configured for:
        1. STAGE_ENTERED trigger for the new stage
        2. STAGE_CHANGED trigger for the workflow

        Then renders and sends each template found
        """
        try:
            logger.info(
                f"Processing stage change for application {event.application_id}: "
                f"{event.previous_stage_id} -> {event.new_stage_id}"
            )

            # Find templates for STAGE_ENTERED event (stage-specific)
            stage_entered_templates = self._email_template_repository.list_by_trigger(
                workflow_id=event.workflow_id,
                trigger_event=TriggerEvent.STAGE_ENTERED,
                stage_id=event.new_stage_id,
                active_only=True
            )

            # Find templates for STAGE_CHANGED event (workflow-wide)
            stage_changed_templates = self._email_template_repository.list_by_trigger(
                workflow_id=event.workflow_id,
                trigger_event=TriggerEvent.STAGE_CHANGED,
                stage_id=None,
                active_only=True
            )

            # Combine all templates
            all_templates = stage_entered_templates + stage_changed_templates

            if not all_templates:
                logger.info(
                    f"No email templates found for workflow {event.workflow_id}, "
                    f"stage {event.new_stage_id}"
                )
                return

            # Build context for template rendering
            context = self._build_email_context(event)

            # Send each template
            for template in all_templates:
                try:
                    # Render subject
                    subject = template.render_subject(context)

                    # Send email via command bus
                    from src.notification.domain.enums.notification_type import NotificationTypeEnum
                    send_email_command = SendEmailCommand(
                        recipient_email=event.candidate_email,
                        subject=subject,
                        template_name=template.template_name,
                        notification_type=NotificationTypeEnum.APPLICATION_CONFIRMATION,
                        template_data=context
                    )

                    self._command_bus.execute(send_email_command)

                    logger.info(
                        f"Sent email '{template.template_name}' to {event.candidate_email} "
                        f"for application {event.application_id}"
                    )

                except Exception as template_error:
                    logger.error(
                        f"Error sending email template {template.id.value} "
                        f"for application {event.application_id}: {str(template_error)}",
                        exc_info=True
                    )
                    # Continue with other templates even if one fails

        except Exception as e:
            logger.error(
                f"Error handling stage change event for application {event.application_id}: {str(e)}",
                exc_info=True
            )
            # Don't re-raise - we don't want to break the application flow

    def _build_email_context(self, event: ApplicationStageChangedEvent) -> Dict[str, Any]:
        """Build context dictionary for template rendering"""
        return {
            'candidate_name': event.candidate_name,
            'candidate_email': event.candidate_email,
            'position_title': event.position_title,
            'company_name': event.company_name,
            'stage_name': event.new_stage_name,
            'previous_stage_id': event.previous_stage_id or 'N/A',
            'new_stage_id': event.new_stage_id,
            'application_id': event.application_id,
            'changed_at': event.changed_at.strftime('%Y-%m-%d %H:%M:%S')
        }
