from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.candidate.domain.entities import CandidateExperience
from src.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class CandidateExperienceDto:
    id: CandidateExperienceId
    candidate_id: CandidateId
    job_title: str
    company: str
    description: Optional[str]
    start_date: date
    end_date: Optional[date]

    @classmethod
    def from_entity(cls, exp: CandidateExperience) -> 'CandidateExperienceDto':
        return cls(
            id=exp.id,
            candidate_id=exp.candidate_id,
            job_title=exp.job_title,
            company=exp.company,
            description=exp.description,
            start_date=exp.start_date,
            end_date=exp.end_date
        )
