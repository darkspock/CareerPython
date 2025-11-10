import dataclasses
from typing import Optional

from adapters.http.candidate.schemas.candidate import CandidateResponse
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.query_bus import Query, QueryHandler
from src.auth_bc.user.domain.value_objects import UserId


@dataclasses.dataclass
class ReadCandidateQuery(Query):
    candidate_id: Optional[CandidateId]
    user_id: Optional[UserId]


class ReadCandidateQueryHandler(QueryHandler[ReadCandidateQuery, Optional[CandidateResponse]]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def handle(self, query: ReadCandidateQuery) -> Optional[CandidateResponse]:
        if query.candidate_id:
            candidate = self.candidate_repository.get_by_id(query.candidate_id)
        elif query.user_id:
            candidate = self.candidate_repository.get_by_user_id(query.user_id)
        else:
            return None

        if candidate:
            return CandidateResponse.model_validate(candidate)
        return None
