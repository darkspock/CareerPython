from typing import Optional

from presentation.candidate.schemas.candidate_experience import CandidateExperienceResponse
from src.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.shared.application.query_bus import Query, QueryHandler


class GetExperienceByIdQuery(Query):
    def __init__(self, id: CandidateExperienceId):
        self.experience_id = id


class GetExperienceByIdQueryHandler(QueryHandler[GetExperienceByIdQuery, Optional[CandidateExperienceResponse]]):
    def __init__(self, experience_repository: CandidateExperienceRepositoryInterface):
        self.experience_repository = experience_repository

    def handle(self, query: GetExperienceByIdQuery) -> Optional[CandidateExperienceResponse]:
        experience = self.experience_repository.get_by_id(query.experience_id)
        if experience:
            return CandidateExperienceResponse.model_validate(experience)
        return None
