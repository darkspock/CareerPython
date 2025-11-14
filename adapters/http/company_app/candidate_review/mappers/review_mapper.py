from adapters.http.company_app.candidate_review.schemas.review_response import ReviewResponse
from src.company_bc.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto


class ReviewResponseMapper:
    """Mapper for converting CandidateReviewDto to Response schema"""

    @staticmethod
    def dto_to_response(dto: CandidateReviewDto) -> ReviewResponse:
        """Convert DTO to response"""
        return ReviewResponse(
            id=dto.id,
            company_candidate_id=dto.company_candidate_id,
            score=dto.score,
            comment=dto.comment,
            workflow_id=dto.workflow_id,
            stage_id=dto.stage_id,
            review_status=dto.review_status,
            created_by_user_id=dto.created_by_user_id,
            created_at=dto.created_at,
            updated_at=dto.updated_at,
            workflow_name=dto.workflow_name,
            stage_name=dto.stage_name,
            created_by_user_name=dto.created_by_user_name,
            created_by_user_email=dto.created_by_user_email,
        )
