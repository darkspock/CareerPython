from dataclasses import dataclass
from datetime import date
from typing import Optional, List

from src.candidate_bc.candidate.application.queries.shared.candidate_dto import CandidateDto
from src.candidate_bc.candidate.domain.enums import CandidateStatusEnum
from src.candidate_bc.candidate.domain.repositories.candidate_repository_interface import CandidateRepositoryInterface
from src.framework.application.query_bus import Query, QueryHandler
from src.framework.domain.enums.job_category import JobCategoryEnum


@dataclass
class AdminListCandidatesQuery(Query):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    status: Optional[CandidateStatusEnum] = None
    job_category: Optional[JobCategoryEnum] = None
    location: Optional[str] = None
    years_of_experience_min: Optional[int] = None
    years_of_experience_max: Optional[int] = None
    created_after: Optional[date] = None
    created_before: Optional[date] = None
    search_term: Optional[str] = None
    has_resume: Optional[bool] = None
    limit: int = 50
    offset: int = 0


class AdminListCandidatesQueryHandler(QueryHandler[AdminListCandidatesQuery, List[CandidateDto]]):
    def __init__(self, candidate_repository: CandidateRepositoryInterface):
        self.candidate_repository = candidate_repository

    def handle(self, query: AdminListCandidatesQuery) -> List[CandidateDto]:
        list = self.candidate_repository.admin_find_by_filters(
            name=query.name,
            email=query.email,
            phone=query.phone,
            status=query.status,
            job_category=query.job_category,
            location=query.location,
            years_of_experience_min=query.years_of_experience_min,
            years_of_experience_max=query.years_of_experience_max,
            created_after=query.created_after,
            created_before=query.created_before,
            search_term=query.search_term,
            has_resume=query.has_resume,
            limit=query.limit,
            offset=query.offset
        )
        return [CandidateDto.from_entity(candidate) for candidate in list]
