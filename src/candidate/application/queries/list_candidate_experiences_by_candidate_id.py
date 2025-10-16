from typing import List

from src.candidate.application.queries.shared.candidate_experience_dto import CandidateExperienceDto
from src.candidate.application.queries.shared.candidate_experience_mapper import CandidateExperienceMapper
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate.infrastructure.repositories.candidate_experience_repository import \
    CandidateExperienceRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


class ListCandidateExperiencesByCandidateIdQuery(Query):
    def __init__(self, candidate_id: CandidateId):
        self.candidate_id = candidate_id


class ListCandidateExperiencesByCandidateIdQueryHandler(
    QueryHandler[ListCandidateExperiencesByCandidateIdQuery, List[CandidateExperienceDto]]):
    def __init__(self, candidate_experience_repository: CandidateExperienceRepositoryInterface):
        self.candidate_experience_repository = candidate_experience_repository

    def handle(self, query: ListCandidateExperiencesByCandidateIdQuery) -> List[CandidateExperienceDto]:
        candidate_experiences = self.candidate_experience_repository.get_all(candidate_id=query.candidate_id)
        return [CandidateExperienceMapper.to_dto(experience) for experience in candidate_experiences]
