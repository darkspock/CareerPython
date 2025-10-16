from dataclasses import dataclass

from core.event import Event
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId


@dataclass
class CandidateProjectDeletedEvent(Event):
    candidate_project_id: str

    @staticmethod
    def create(id: CandidateProjectId) -> 'CandidateProjectDeletedEvent':
        return CandidateProjectDeletedEvent(candidate_project_id=id.value)
