from typing import List

from adapters.http.candidate_app.schemas.candidate_education import CandidateEducationResponse
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.query_bus import Query, QueryHandler


class GetEducationsByCandidateIdQuery(Query):
    def __init__(self, candidate_id: CandidateId):
        self.candidate_id = candidate_id


class GetEducationsByCandidateIdQueryHandler(
    QueryHandler[GetEducationsByCandidateIdQuery, List[CandidateEducationResponse]]):
    def __init__(self, education_repository: CandidateEducationRepositoryInterface):
        self.education_repository = education_repository

    def handle(self, query: GetEducationsByCandidateIdQuery) -> List[CandidateEducationResponse]:
        educations = self.education_repository.get_by_candidate_id(query.candidate_id)
        return [CandidateEducationResponse.model_validate(edu) for edu in educations]
