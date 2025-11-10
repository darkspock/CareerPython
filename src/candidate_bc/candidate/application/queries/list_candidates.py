from typing import List, Optional

from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.application.queries.shared.candidate_dto_mapper import CandidateDtoMapper
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


class ListCandidatesQuery(Query):
    def __init__(self, name: Optional[str] = None, phone: Optional[str] = None):
        self.name = name
        self.phone = phone


class ListCandidatesQueryHandler(QueryHandler[ListCandidatesQuery, List[CandidateDto]]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def handle(self, query: ListCandidatesQuery) -> List[CandidateDto]:
        candidates = self.candidate_repository.get_all(name=query.name, phone=query.phone)
        return [CandidateDtoMapper.from_model(candidate) for candidate in candidates]
