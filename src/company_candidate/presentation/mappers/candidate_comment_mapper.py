from src.company_candidate.application.dtos.candidate_comment_dto import CandidateCommentDto
from src.company_candidate.presentation.schemas.candidate_comment_response import CandidateCommentResponse


class CandidateCommentResponseMapper:
    """Mapper for candidate comment between DTO and response"""

    @staticmethod
    def dto_to_response(dto: CandidateCommentDto) -> CandidateCommentResponse:
        """Convert DTO to response"""
        return CandidateCommentResponse(
            id=dto.id,
            company_candidate_id=dto.company_candidate_id,
            comment=dto.comment,
            workflow_id=dto.workflow_id,
            stage_id=dto.stage_id,
            created_by_user_id=dto.created_by_user_id,
            review_status=dto.review_status,
            visibility=dto.visibility,
            created_at=dto.created_at,
            updated_at=dto.updated_at
        )
