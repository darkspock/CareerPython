from dataclasses import dataclass

from core.event import Event
from src.candidate_bc.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId


@dataclass
class CandidateExperienceDeletedEvent(Event):
    candidate_experience_id: str

    @staticmethod
    def create(id: CandidateExperienceId) -> 'CandidateExperienceDeletedEvent':
        return CandidateExperienceDeletedEvent(candidate_experience_id=id.value)
