from dataclasses import dataclass

from src.shared.application.query import Query


@dataclass(frozen=True)
class ListCompanyCandidatesByCandidateQuery(Query):
    """Query to list all company candidates for a specific candidate"""
    candidate_id: str
