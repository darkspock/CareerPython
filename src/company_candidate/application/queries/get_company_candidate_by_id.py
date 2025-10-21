from dataclasses import dataclass

from src.shared.application.query import Query


@dataclass(frozen=True)
class GetCompanyCandidateByIdQuery(Query):
    """Query to get a company candidate by ID"""
    id: str
