from core.config import settings
from src.company_bc.company.application.dtos.company_user_invitation_dto import CompanyUserInvitationDto
from adapters.http.company_app.company.schemas.company_user_invitation_response import (
    CompanyUserInvitationResponse,
    UserInvitationLinkResponse
)


class CompanyUserInvitationResponseMapper:
    """Mapper for converting CompanyUserInvitationDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CompanyUserInvitationDto) -> CompanyUserInvitationResponse:
        """Convert DTO to response with invitation link"""
        invitation_link = f"{settings.FRONTEND_URL}/invitations/accept?token={dto.token}"
        
        return CompanyUserInvitationResponse(
            id=dto.id,
            company_id=dto.company_id,
            email=dto.email,
            invited_by_user_id=dto.invited_by_user_id,
            token=dto.token,
            status=dto.status,
            expires_at=dto.expires_at,
            accepted_at=dto.accepted_at,
            rejected_at=dto.rejected_at,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            invitation_link=invitation_link,
        )

    @staticmethod
    def dto_to_link_response(dto: CompanyUserInvitationDto) -> UserInvitationLinkResponse:
        """Convert DTO to link response for sharing"""
        invitation_link = f"{settings.FRONTEND_URL}/invitations/accept?token={dto.token}"
        
        return UserInvitationLinkResponse(
            invitation_id=dto.id,
            invitation_link=invitation_link,
            expires_at=dto.expires_at,
            email=dto.email,
        )

