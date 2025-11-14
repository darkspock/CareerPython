from typing import List

from src.candidate_bc.candidate.application.queries.shared.candidate_project_dto import CandidateProjectDto
from src.candidate_bc.candidate.application.queries.shared.candidate_project_mapper import CandidateProjectMapper
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.infrastructure.repositories.candidate_project_repository import CandidateProjectRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler


class ListCandidateProjectsByCandidateIdQuery(Query):
    def __init__(self, candidate_id: CandidateId):
        self.candidate_id = candidate_id


class ListCandidateProjectsByCandidateIdQueryHandler(
    QueryHandler[ListCandidateProjectsByCandidateIdQuery, List[CandidateProjectDto]]):
    def __init__(self, candidate_project_repository: CandidateProjectRepositoryInterface):
        self.candidate_project_repository = candidate_project_repository

    def handle(self, query: ListCandidateProjectsByCandidateIdQuery) -> List[CandidateProjectDto]:
        candidate_projects = self.candidate_project_repository.get_all(candidate_id=query.candidate_id)
        return [CandidateProjectMapper.to_dto(project) for project in candidate_projects]
