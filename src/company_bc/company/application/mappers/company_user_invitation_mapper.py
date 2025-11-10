from src.company_bc.company.application.dtos.company_user_invitation_dto import CompanyUserInvitationDto
from src.company_bc.company.domain.entities.company_user_invitation import CompanyUserInvitation


class CompanyUserInvitationMapper:
    """Mapper for converting CompanyUserInvitation entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CompanyUserInvitation) -> CompanyUserInvitationDto:
        """Convert entity to DTO"""
        return CompanyUserInvitationDto(
            id=str(entity.id),
            company_id=str(entity.company_id),
            email=entity.email,
            invited_by_user_id=str(entity.invited_by_user_id),
            token=str(entity.token),
            status=entity.status.value,
            expires_at=entity.expires_at,
            accepted_at=entity.accepted_at,
            rejected_at=entity.rejected_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

