from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional

from src.candidate_bc.candidate.domain.entities import CandidateEducation
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class CandidateEducationDto:
    id: CandidateEducationId
    candidate_id: CandidateId
    institution: str
    degree: str
    description: str
    start_date: date
    end_date: Optional[date]
    created_at: datetime
    updated_at: datetime

    @classmethod
    def from_entity(cls, edu: CandidateEducation) -> 'CandidateEducationDto':
        return cls(
            id=edu.id,
            candidate_id=edu.candidate_id,
            institution=edu.institution,
            degree=edu.degree,
            description=edu.description,
            start_date=edu.start_date,
            end_date=edu.end_date,
            created_at=edu.created_at,
            updated_at=edu.updated_at
        )
