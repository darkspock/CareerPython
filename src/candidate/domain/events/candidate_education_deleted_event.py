from dataclasses import dataclass

from core.event import Event
from src.candidate.domain.value_objects.candidate_education_id import CandidateEducationId


@dataclass
class CandidateEducationDeletedEvent(Event):
    candidate_education_id: str

    @staticmethod
    def create(id: CandidateEducationId) -> 'CandidateEducationDeletedEvent':
        return CandidateEducationDeletedEvent(candidate_education_id=id.value)
