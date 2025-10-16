from dataclasses import dataclass, field
from datetime import date, datetime
from typing import Optional

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId


@dataclass
class CandidateProject:
    """Entidad del dominio para proyectos de candidatos"""
    id: CandidateProjectId
    candidate_id: CandidateId
    name: str
    description: str
    start_date: date
    end_date: Optional[date] = None
    created_at: datetime = field(default_factory=datetime.now)
    updated_at: datetime = field(default_factory=datetime.now)

    @staticmethod
    def create(
            id: CandidateProjectId,
            candidate_id: CandidateId,
            name: str,
            description: str,
            start_date: date,
            end_date: Optional[date]
    ) -> 'CandidateProject':
        return CandidateProject(
            id=id,
            candidate_id=candidate_id,
            name=name,
            description=description,
            start_date=start_date,
            end_date=end_date
        )

    def update_details(self, name: str, description: str, start_date: date, end_date: Optional[date]) -> None:
        """Actualiza los detalles del proyecto del candidato"""
        self.name = name
        self.description = description
        self.start_date = start_date
        self.end_date = end_date
        self.updated_at = datetime.now()
