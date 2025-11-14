from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.application.dtos.company_user_invitation_dto import CompanyUserInvitationDto
from src.company_bc.company.application.mappers.company_user_invitation_mapper import CompanyUserInvitationMapper
from src.company_bc.company.domain.value_objects import CompanyId
from src.company_bc.company.domain.infrastructure.company_user_invitation_repository_interface import (
    CompanyUserInvitationRepositoryInterface
)
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetInvitationByEmailAndCompanyQuery(Query):
    """Query to get a user invitation by email and company"""
    email: str
    company_id: CompanyId


class GetInvitationByEmailAndCompanyQueryHandler(
    QueryHandler[GetInvitationByEmailAndCompanyQuery, Optional[CompanyUserInvitationDto]]
):
    """Handler for getting a user invitation by email and company - returns DTO or None"""

    def __init__(self, invitation_repository: CompanyUserInvitationRepositoryInterface):
        self.invitation_repository = invitation_repository

    def handle(self, query: GetInvitationByEmailAndCompanyQuery) -> Optional[CompanyUserInvitationDto]:
        """Execute the query - returns DTO or None"""
        invitation = self.invitation_repository.get_by_email_and_company(
            query.email.lower(),
            query.company_id
        )

        if not invitation:
            return None

        return CompanyUserInvitationMapper.entity_to_dto(invitation)

