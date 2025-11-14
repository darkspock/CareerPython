"""
List Email Templates By Stage Query
Phase 7: Query to list email templates by stage
"""

from dataclasses import dataclass
from typing import List

from src.framework.application.query_bus import Query, QueryHandler
from src.notification_bc.email_template.application.dtos.email_template_dto import EmailTemplateDto
from src.notification_bc.email_template.domain.repositories.email_template_repository_interface import \
    EmailTemplateRepositoryInterface


@dataclass(frozen=True)
class ListEmailTemplatesByStageQuery(Query):
    """Query to list email templates by stage"""
    stage_id: str
    active_only: bool = False


class ListEmailTemplatesByStageQueryHandler(QueryHandler[ListEmailTemplatesByStageQuery, List[EmailTemplateDto]]):
    """Handler for ListEmailTemplatesByStageQuery"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListEmailTemplatesByStageQuery) -> List[EmailTemplateDto]:
        """Handle the list email templates by stage query"""
        templates = self._repository.list_by_stage(
            stage_id=query.stage_id,
            active_only=query.active_only
        )

        return [EmailTemplateDto.from_entity(template) for template in templates]
