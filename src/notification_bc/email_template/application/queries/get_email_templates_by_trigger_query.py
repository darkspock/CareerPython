"""
Get Email Templates By Trigger Query
Phase 7: Query to get email templates by trigger event
"""

from dataclasses import dataclass
from typing import List, Optional

from src.notification_bc.email_template.application.dtos.email_template_dto import EmailTemplateDto
from src.notification_bc.email_template.domain.enums.trigger_event import TriggerEvent
from src.notification_bc.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetEmailTemplatesByTriggerQuery(Query):
    """Query to get email templates by trigger event"""
    workflow_id: str
    trigger_event: TriggerEvent
    stage_id: Optional[str] = None
    active_only: bool = True


class GetEmailTemplatesByTriggerQueryHandler(QueryHandler[GetEmailTemplatesByTriggerQuery, List[EmailTemplateDto]]):
    """Handler for GetEmailTemplatesByTriggerQuery"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetEmailTemplatesByTriggerQuery) -> List[EmailTemplateDto]:
        """Handle the get email templates by trigger query"""
        templates = self._repository.list_by_trigger(
            workflow_id=query.workflow_id,
            trigger_event=query.trigger_event,
            stage_id=query.stage_id,
            active_only=query.active_only
        )

        return [EmailTemplateDto.from_entity(template) for template in templates]
