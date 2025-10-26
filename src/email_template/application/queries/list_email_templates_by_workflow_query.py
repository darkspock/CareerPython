"""
List Email Templates By Workflow Query
Phase 7: Query to list email templates by workflow
"""

from dataclasses import dataclass
from typing import List

from src.email_template.application.dtos.email_template_dto import EmailTemplateDto
from src.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class ListEmailTemplatesByWorkflowQuery(Query):
    """Query to list email templates by workflow"""
    workflow_id: str
    active_only: bool = False


class ListEmailTemplatesByWorkflowQueryHandler(QueryHandler[ListEmailTemplatesByWorkflowQuery, List[EmailTemplateDto]]):
    """Handler for ListEmailTemplatesByWorkflowQuery"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def handle(self, query: ListEmailTemplatesByWorkflowQuery) -> List[EmailTemplateDto]:
        """Handle the list email templates by workflow query"""
        templates = self._repository.list_by_workflow(
            workflow_id=query.workflow_id,
            active_only=query.active_only
        )

        return [EmailTemplateDto.from_entity(template) for template in templates]
