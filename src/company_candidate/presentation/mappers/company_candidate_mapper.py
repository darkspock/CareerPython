from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.presentation.schemas.company_candidate_response import CompanyCandidateResponse


class CompanyCandidateResponseMapper:
    """Mapper for converting CompanyCandidateDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CompanyCandidateDto) -> CompanyCandidateResponse:
        """Convert DTO to response"""
        return CompanyCandidateResponse(
            id=dto.id,
            company_id=dto.company_id,
            candidate_id=dto.candidate_id,
            status=dto.status,
            ownership_status=dto.ownership_status,
            created_by_user_id=dto.created_by_user_id,
            workflow_id=dto.workflow_id,
            current_stage_id=dto.current_stage_id,
            phase_id=dto.phase_id,
            invited_at=dto.invited_at,
            confirmed_at=dto.confirmed_at,
            rejected_at=dto.rejected_at,
            archived_at=dto.archived_at,
            visibility_settings=dto.visibility_settings,
            tags=dto.tags,
            position=dto.position,
            department=dto.department,
            priority=dto.priority,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
        )
