from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_application.domain.enums.application_status import ApplicationStatusEnum
from src.candidate_application.domain.value_objects.candidate_application_id import CandidateApplicationId
from src.job_position.domain.value_objects.job_position_id import JobPositionId


@dataclass
class CandidateApplication:
    """Entidad del dominio para aplicaciones de candidatos a posiciones"""
    id: CandidateApplicationId
    candidate_id: CandidateId
    job_position_id: JobPositionId
    application_status: ApplicationStatusEnum
    applied_at: datetime
    updated_at: Optional[datetime] = None
    notes: Optional[str] = None

    def approve(self) -> None:
        """Aprobar la aplicación"""
        self.application_status = ApplicationStatusEnum.ACCEPTED
        self.updated_at = datetime.utcnow()

    def reject(self, notes: Optional[str] = None) -> None:
        """Rechazar la aplicación"""
        self.application_status = ApplicationStatusEnum.REJECTED
        self.updated_at = datetime.utcnow()
        if notes:
            self.notes = notes

    def start_review(self) -> None:
        """Iniciar revisión de la aplicación"""
        self.application_status = ApplicationStatusEnum.REVIEWING
        self.updated_at = datetime.utcnow()

    def mark_interviewed(self) -> None:
        """Marcar como entrevistado"""
        self.application_status = ApplicationStatusEnum.INTERVIEWED
        self.updated_at = datetime.utcnow()

    def withdraw(self) -> None:
        """Retirar la aplicación"""
        self.application_status = ApplicationStatusEnum.WITHDRAWN
        self.updated_at = datetime.utcnow()

    def update_notes(self, notes: str) -> None:
        """Actualizar notas de la aplicación"""
        self.notes = notes
        self.updated_at = datetime.utcnow()

    @staticmethod
    def create(
            id: CandidateApplicationId,
            candidate_id: CandidateId,
            job_position_id: JobPositionId,
            notes: Optional[str] = None
    ) -> 'CandidateApplication':
        """Factory method para crear una nueva aplicación"""
        now = datetime.utcnow()
        return CandidateApplication(
            id=id,
            candidate_id=candidate_id,
            job_position_id=job_position_id,
            application_status=ApplicationStatusEnum.APPLIED,
            applied_at=now,
            updated_at=now,  # Set updated_at to creation time
            notes=notes
        )
