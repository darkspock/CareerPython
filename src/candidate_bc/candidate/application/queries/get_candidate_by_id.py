from dataclasses import dataclass
from typing import Optional

from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.application.queries.shared.candidate_dto_mapper import CandidateDtoMapper
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.query_bus import Query, QueryHandler


@dataclass
class GetCandidateByIdQuery(Query):
    id: CandidateId


class GetCandidateByIdQueryHandler(QueryHandler[GetCandidateByIdQuery, Optional[CandidateDto]]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def handle(self, query: GetCandidateByIdQuery) -> Optional[CandidateDto]:
        candidate = self.candidate_repository.get_by_id(query.id)
        if candidate:
            return CandidateDtoMapper.from_model(candidate)
        return None
