from src.company_candidate.domain.entities.candidate_comment import CandidateComment
from src.company_candidate.application.dtos.candidate_comment_dto import CandidateCommentDto


class CandidateCommentMapper:
    """Mapper for converting between CandidateComment entity and DTO"""

    @staticmethod
    def entity_to_dto(entity: CandidateComment) -> CandidateCommentDto:
        """Convert CandidateComment entity to DTO"""
        return CandidateCommentDto(
            id=str(entity.id),
            company_candidate_id=str(entity.company_candidate_id),
            comment=entity.comment,
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            stage_id=str(entity.stage_id) if entity.stage_id else None,
            created_by_user_id=str(entity.created_by_user_id),
            review_status=entity.review_status.value,
            visibility=entity.visibility.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )

