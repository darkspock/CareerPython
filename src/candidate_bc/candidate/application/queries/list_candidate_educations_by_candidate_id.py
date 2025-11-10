from typing import List

from src.candidate_bc.candidate.application.queries.shared.candidate_education_dto import CandidateEducationDto
from src.candidate_bc.candidate.application.queries.shared.candidate_education_mapper import CandidateEducationMapper
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.infrastructure.repositories.candidate_education_repository import \
    SQLAlchemyCandidateEducationRepository
from src.framework.application.query_bus import Query, QueryHandler


class ListCandidateEducationsByCandidateIdQuery(Query):
    def __init__(self, candidate_id: CandidateId):
        self.candidate_id = candidate_id


class ListCandidateEducationsByCandidateIdQueryHandler(
    QueryHandler[ListCandidateEducationsByCandidateIdQuery, List[CandidateEducationDto]]):
    def __init__(self, candidate_education_repository: SQLAlchemyCandidateEducationRepository):
        self.candidate_education_repository = candidate_education_repository

    def handle(self, query: ListCandidateEducationsByCandidateIdQuery) -> List[CandidateEducationDto]:
        candidate_educations = self.candidate_education_repository.get_all(candidate_id=query.candidate_id)
        return [CandidateEducationMapper.to_dto(education) for education in candidate_educations]
