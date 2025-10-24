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
            workflow_id=str(entity.workflow_id) if entity.workflow_id else None,
            current_stage_id=str(entity.current_stage_id) if entity.current_stage_id else None,
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
            lead_id=entity.lead_id,
            source=entity.source,
            resume_url=entity.resume_url,
            resume_uploaded_by=str(entity.resume_uploaded_by) if entity.resume_uploaded_by else None,
            resume_uploaded_at=entity.resume_uploaded_at,
            created_at=entity.created_at,
            updated_at=entity.updated_at,
        )
