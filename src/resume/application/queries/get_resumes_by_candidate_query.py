from dataclasses import dataclass
from typing import Optional, List

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.resume.domain.enums.resume_type import ResumeType
from src.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.resume.presentation.schemas.resume_dto import ResumeDto
from src.shared.application.query_bus import Query, QueryHandler


@dataclass
class GetResumesByCandidateQuery(Query):
    """Query para obtener resumes por candidato"""
    candidate_id: CandidateId
    resume_type: Optional[ResumeType] = None
    limit: Optional[int] = None


class GetResumesByCandidateQueryHandler(QueryHandler[GetResumesByCandidateQuery, List[ResumeDto]]):
    """Handler para obtener resumes por candidato"""

    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.resume_repository = resume_repository

    def handle(self, query: GetResumesByCandidateQuery) -> List[ResumeDto]:
        """Maneja la query de obtener resumes por candidato"""

        # Obtener resumes del repositorio
        resumes = self.resume_repository.get_by_candidate_id(
            candidate_id=query.candidate_id,
            resume_type=query.resume_type,
            limit=query.limit
        )

        # Convertir a DTOs
        return [ResumeDto.from_entity(resume) for resume in resumes]
