from src.candidate_application.application.queries.shared.candidate_application_dto import CandidateApplicationDto
from src.candidate_application.domain.entities.candidate_application import CandidateApplication


class CandidateApplicationDtoMapper:
    """Mapper para convertir entidades a DTOs"""

    @staticmethod
    def from_entity(entity: CandidateApplication) -> CandidateApplicationDto:
        """Convierte entidad de dominio a DTO"""
        return CandidateApplicationDto(
            id=entity.id.value,
            candidate_id=entity.candidate_id.value,
            job_position_id=entity.job_position_id.value,
            application_status=entity.application_status,
            applied_at=entity.applied_at,
            updated_at=entity.updated_at,
            notes=entity.notes
        )
