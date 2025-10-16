from typing import Optional

from src.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate.application.queries.shared.candidate_dto_mapper import CandidateDtoMapper
from src.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler
from src.user.domain.value_objects.UserId import UserId


class GetCandidateByUserIdQuery(Query):
    def __init__(self, user_id: UserId):
        self.user_id = user_id


class GetCandidateByUserIdQueryHandler(QueryHandler[GetCandidateByUserIdQuery, Optional[CandidateDto]]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def handle(self, query: GetCandidateByUserIdQuery) -> Optional[CandidateDto]:
        candidate = self.candidate_repository.get_by_user_id(query.user_id)
        if candidate:
            return CandidateDtoMapper.from_model(candidate)
        return None
