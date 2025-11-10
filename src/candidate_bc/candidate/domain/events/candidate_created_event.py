from dataclasses import dataclass

from core.event import Event
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class CandidateCreatedEvent(Event):
    candidate_id: str

    @staticmethod
    def create(id: CandidateId) -> 'CandidateCreatedEvent':
        return CandidateCreatedEvent(candidate_id=id.value)
