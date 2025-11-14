from typing import Optional

from src.candidate_bc.candidate.application.queries.shared.candidate_education_dto import CandidateEducationDto
from src.candidate_bc.candidate.application.queries.shared.candidate_education_mapper import CandidateEducationMapper
from src.candidate_bc.candidate.domain.exceptions import CandidateNotFoundError
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.framework.application.query_bus import Query, QueryHandler


class GetEducationByIdQuery(Query):
    def __init__(self, education_id: CandidateEducationId):
        self.education_id = education_id


class GetEducationByIdQueryHandler(QueryHandler[GetEducationByIdQuery, Optional[CandidateEducationDto]]):
    def __init__(self, education_repository: CandidateEducationRepositoryInterface):
        self.education_repository = education_repository

    def handle(self, query: GetEducationByIdQuery) -> Optional[CandidateEducationDto]:
        education = self.education_repository.get_by_id(query.education_id)
        if not education:
            raise CandidateNotFoundError(f"Education with id {query.education_id} not found")
        return CandidateEducationMapper.to_dto(education)
