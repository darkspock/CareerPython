from src.candidate.application.queries.shared.candidate_project_dto import CandidateProjectDto
from src.candidate.application.queries.shared.candidate_project_mapper import CandidateProjectMapper
from src.candidate.domain.exceptions import CandidateNotFoundError
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from src.candidate.infrastructure.repositories.candidate_project_repository import CandidateProjectRepositoryInterface
from src.shared.application.query_bus import Query, QueryHandler


class GetProjectByIdQuery(Query):
    def __init__(self, id: CandidateProjectId):
        self.project_id = id


class GetProjectByIdQueryHandler(QueryHandler[GetProjectByIdQuery, CandidateProjectDto]):
    def __init__(self, project_repository: CandidateProjectRepositoryInterface):
        self.project_repository = project_repository

    def handle(self, query: GetProjectByIdQuery) -> CandidateProjectDto:
        project = self.project_repository.get_by_id(query.project_id)
        if not project:
            raise CandidateNotFoundError(f"Project with id {query.project_id} not found")
        return CandidateProjectMapper.to_dto(project)
