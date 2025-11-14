from dataclasses import dataclass

from core.event import Event
from src.candidate_bc.candidate.domain.value_objects.candidate_project_id import CandidateProjectId


@dataclass
class CandidateProjectCreatedEvent(Event):
    candidate_project_id: str

    @staticmethod
    def create(id: CandidateProjectId) -> 'CandidateProjectCreatedEvent':
        return CandidateProjectCreatedEvent(candidate_project_id=id.value)
