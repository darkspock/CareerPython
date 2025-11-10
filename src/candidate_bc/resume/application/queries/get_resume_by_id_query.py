from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.candidate_bc.resume.domain.value_objects.resume_id import ResumeId
from src.candidate_bc.resume.application.dtos.resume_dto import ResumeDto
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetResumeByIdQuery(Query):
    """Query para obtener un resume por ID"""
    resume_id: ResumeId


class GetResumeByIdQueryHandler(QueryHandler[GetResumeByIdQuery, Optional[ResumeDto]]):
    """Handler para obtener un resume por ID"""

    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.resume_repository = resume_repository

    def handle(self, query: GetResumeByIdQuery) -> Optional[ResumeDto]:
        """Maneja la query de obtener resume por ID"""

        # Obtener resume del repositorio
        resume = self.resume_repository.get_by_id(query.resume_id)

        # Convertir a DTO si existe
        return ResumeDto.from_entity(resume) if resume else None
