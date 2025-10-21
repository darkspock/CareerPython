from dataclasses import dataclass

from src.shared.application.query import Query


@dataclass(frozen=True)
class GetCompanyCandidateByCompanyAndCandidateQuery(Query):
    """Query to get a company candidate by company ID and candidate ID"""
    company_id: str
    candidate_id: str
