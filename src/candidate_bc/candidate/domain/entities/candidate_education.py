from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId


@dataclass
class CandidateEducation:
    """Entidad del dominio para educación de candidatos"""
    id: CandidateEducationId
    candidate_id: CandidateId
    degree: str
    institution: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(
            id: CandidateEducationId,
            candidate_id: CandidateId,
            degree: str,
            institution: str,
            description: str,
            start_date: date,
            end_date: Optional[date]
    ) -> 'CandidateEducation':
        return CandidateEducation(
            id=id,
            candidate_id=candidate_id,
            degree=degree,
            institution=institution,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

    def update_details(self, degree: str, institution: str, description: str, start_date: date,
                       end_date: Optional[date]) -> None:
        """Actualiza los detalles de la educación del candidato"""
        self.degree = degree
        self.institution = institution
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.updated_at = datetime.now()
