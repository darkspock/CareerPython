"""
Get Email Template By ID Query
Phase 7: Query to get an email template by ID
"""

from dataclasses import dataclass
from typing import Optional

from src.notification_bc.email_template.application.dtos.email_template_dto import EmailTemplateDto
from src.notification_bc.email_template.domain.value_objects.email_template_id import EmailTemplateId
from src.notification_bc.email_template.domain.repositories.email_template_repository_interface import EmailTemplateRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


@dataclass(frozen=True)
class GetEmailTemplateByIdQuery(Query):
    """Query to get an email template by ID"""
    template_id: str


class GetEmailTemplateByIdQueryHandler(QueryHandler[GetEmailTemplateByIdQuery, Optional[EmailTemplateDto]]):
    """Handler for GetEmailTemplateByIdQuery"""

    def __init__(self, repository: EmailTemplateRepositoryInterface):
        self._repository = repository

    def handle(self, query: GetEmailTemplateByIdQuery) -> Optional[EmailTemplateDto]:
        """Handle the get email template by ID query"""
        template_id = EmailTemplateId.from_string(query.template_id)
        template = self._repository.get_by_id(template_id)

        if not template:
            return None

        return EmailTemplateDto.from_entity(template)
