from src.company_bc.candidate_review.application.dtos.candidate_review_dto import CandidateReviewDto
from src.company_bc.candidate_review.domain.entities.candidate_review import CandidateReview


class CandidateReviewMapper:
    """Mapper for converting CandidateReview entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CandidateReview) -> CandidateReviewDto:
        """Convert entity to DTO"""
        return CandidateReviewDto(
            id=str(entity.id),
            company_candidate_id=str(entity.company_candidate_id),
            score=entity.score.value,
            comment=entity.comment,
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            stage_id=str(entity.stage_id) if entity.stage_id else None,
            review_status=entity.review_status.value,
            created_by_user_id=str(entity.created_by_user_id),
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

    @staticmethod
    def from_entity(entity: CandidateReview) -> CandidateReviewDto:
        """Alias for entity_to_dto for consistency"""
        return CandidateReviewMapper.entity_to_dto(entity)

