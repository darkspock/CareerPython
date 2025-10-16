from dataclasses import dataclass
from typing import Optional

from src.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate.application.queries.shared.candidate_dto_mapper import CandidateDtoMapper
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.shared.application.query_bus import Query, QueryHandler


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
