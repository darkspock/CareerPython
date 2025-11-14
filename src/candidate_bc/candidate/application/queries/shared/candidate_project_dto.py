from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.candidate_bc.candidate.domain.entities import CandidateProject
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.domain.value_objects.candidate_project_id import CandidateProjectId


@dataclass
class CandidateProjectDto:
    id: CandidateProjectId
    candidate_id: CandidateId
    name: str
    description: str
    start_date: date
    end_date: Optional[date]

    @classmethod
    def from_entity(cls, proj: CandidateProject) -> 'CandidateProjectDto':
        return cls(
            id=proj.id,
            candidate_id=proj.candidate_id,
            name=proj.name,
            description=proj.description,
            start_date=proj.start_date,
            end_date=proj.end_date
        )
