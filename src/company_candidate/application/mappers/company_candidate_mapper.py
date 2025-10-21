from src.company_candidate.application.dtos.company_candidate_dto import CompanyCandidateDto
from src.company_candidate.domain.entities.company_candidate import CompanyCandidate


class CompanyCandidateMapper:
    """Mapper for converting CompanyCandidate entities to DTOs"""

    @staticmethod
    def entity_to_dto(entity: CompanyCandidate) -> CompanyCandidateDto:
        """Convert entity to DTO"""
        return CompanyCandidateDto(
            id=str(entity.id),
            company_id=str(entity.company_id),
            candidate_id=str(entity.candidate_id),
            status=entity.status.value,
            ownership_status=entity.ownership_status.value,
            created_by_user_id=str(entity.created_by_user_id),
            workflow_id=entity.workflow_id,
            current_stage_id=entity.current_stage_id,
            invited_at=entity.invited_at,
            confirmed_at=entity.confirmed_at,
            rejected_at=entity.rejected_at,
            archived_at=entity.archived_at,
            visibility_settings=entity.visibility_settings.to_dict(),
            tags=entity.tags,
            internal_notes=entity.internal_notes,
            position=entity.position,
            department=entity.department,
            priority=entity.priority.value,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
