from dataclasses import dataclass

from src.shared.application.query import Query


@dataclass(frozen=True)
class ListCompanyCandidatesByCompanyQuery(Query):
    """Query to list all company candidates for a specific company"""
    company_id: str
