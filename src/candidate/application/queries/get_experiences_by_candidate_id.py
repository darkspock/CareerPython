from typing import List

from presentation.candidate.schemas.candidate_experience import CandidateExperienceResponse
from src.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.shared.application.query_bus import Query, QueryHandler


class GetExperiencesByCandidateIdQuery(Query):
    def __init__(self, candidate_id: CandidateId):
        self.candidate_id = candidate_id


class GetExperiencesByCandidateIdQueryHandler(
    QueryHandler[GetExperiencesByCandidateIdQuery, List[CandidateExperienceResponse]]):
    def __init__(self, experience_repository: CandidateExperienceRepositoryInterface):
        self.experience_repository = experience_repository

    def handle(self, query: GetExperiencesByCandidateIdQuery) -> List[CandidateExperienceResponse]:
        experiences = self.experience_repository.get_by_candidate_id(query.candidate_id)
        return [CandidateExperienceResponse.model_validate(exp) for exp in experiences]
