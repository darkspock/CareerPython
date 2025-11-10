import dataclasses
from typing import Optional

from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.application.queries.shared.candidate_dto_mapper import CandidateDtoMapper
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.query_bus import Query, QueryHandler
from src.auth_bc.user.domain.value_objects import UserId


@dataclasses.dataclass
class ReadCandidateQuery(Query):
    candidate_id: Optional[CandidateId]
    user_id: Optional[UserId]


class ReadCandidateQueryHandler(QueryHandler[ReadCandidateQuery, Optional[CandidateDto]]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def handle(self, query: ReadCandidateQuery) -> Optional[CandidateDto]:
        if query.candidate_id:
            candidate = self.candidate_repository.get_by_id(query.candidate_id)
        elif query.user_id:
            candidate = self.candidate_repository.get_by_user_id(query.user_id)
        else:
            return None

        if candidate:
            return CandidateDtoMapper.from_model(candidate)
        return None
