from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from src.candidate_bc.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class CandidateExperience:
    """Entidad del dominio para experiencia laboral de candidatos"""
    id: CandidateExperienceId
    candidate_id: CandidateId
    job_title: str
    company: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(
            id: CandidateExperienceId,
            candidate_id: CandidateId,
            job_title: str,
            company: str,
            description: str,
            start_date: date,
            end_date: Optional[date]
    ) -> 'CandidateExperience':
        return CandidateExperience(
            id=id,
            candidate_id=candidate_id,
            job_title=job_title,
            company=company,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

    def update_details(self, job_title: str, company: str, description: str, start_date: date,
                       end_date: Optional[date]) -> None:
        """Actualiza los detalles de la experiencia laboral del candidato"""
        self.job_title = job_title
        self.company = company
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.updated_at = datetime.now()
