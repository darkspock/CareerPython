from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.application.dtos.company_user_invitation_dto import CompanyUserInvitationDto
from src.company_bc.company.application.mappers.company_user_invitation_mapper import CompanyUserInvitationMapper
from src.company_bc.company.domain.infrastructure.company_user_invitation_repository_interface import (
    CompanyUserInvitationRepositoryInterface
)
from src.company_bc.company.domain.value_objects.invitation_token import InvitationToken
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetUserInvitationQuery(Query):
    """Query to get a user invitation by token"""
    token: InvitationToken


class GetUserInvitationQueryHandler(QueryHandler[GetUserInvitationQuery, Optional[CompanyUserInvitationDto]]):
    """Handler for getting a user invitation - returns DTO or None"""

    def __init__(self, invitation_repository: CompanyUserInvitationRepositoryInterface):
        self.invitation_repository = invitation_repository

    def handle(self, query: GetUserInvitationQuery) -> Optional[CompanyUserInvitationDto]:
        """Execute the query - returns DTO or None"""
        invitation = self.invitation_repository.get_by_token(query.token)

        if not invitation:
            return None

        return CompanyUserInvitationMapper.entity_to_dto(invitation)
