from typing import List

from adapters.http.candidate_app.schemas.candidate_project import CandidateProjectResponse
from src.candidate_bc.candidate.domain.repositories.candidate_project_repository_interface import \
    CandidateProjectRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.framework.application.query_bus import Query, QueryHandler


class GetProjectsByCandidateIdQuery(Query):
    def __init__(self, candidate_id: CandidateId):
        self.candidate_id = candidate_id


class GetProjectsByCandidateIdQueryHandler(QueryHandler[GetProjectsByCandidateIdQuery, List[CandidateProjectResponse]]):
    def __init__(self, project_repository: CandidateProjectRepositoryInterface):
        self.project_repository = project_repository

    def handle(self, query: GetProjectsByCandidateIdQuery) -> List[CandidateProjectResponse]:
        projects = self.project_repository.get_by_candidate_id(query.candidate_id)
        return [CandidateProjectResponse.model_validate(proj) for proj in projects]
