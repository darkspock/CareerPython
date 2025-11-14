from dataclasses import dataclass

from core.event import Event
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId


@dataclass
class CandidateEducationCreatedEvent(Event):
    candidate_education_id: str

    @staticmethod
    def create(id: CandidateEducationId) -> 'CandidateEducationCreatedEvent':
        return CandidateEducationCreatedEvent(candidate_education_id=id.value)
