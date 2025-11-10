from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.candidate_bc.candidate.domain.exceptions import EducationNotFoundError
from src.candidate_bc.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class UpdateEducationCommand(Command):
    id: CandidateEducationId
    degree: str
    institution: str
    description: str
    start_date: date
    end_date: Optional[date]


class UpdateEducationCommandHandler(CommandHandler[UpdateEducationCommand]):
    def __init__(self, education_repository: CandidateEducationRepositoryInterface):
        self.education_repository = education_repository

    def execute(self, command: UpdateEducationCommand) -> None:
        existing_education = self.education_repository.get_by_id(command.id)
        if not existing_education:
            raise EducationNotFoundError("Education not found")
        existing_education.update_details(
            degree=command.degree,
            institution=command.institution,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date
        )

        self.education_repository.update(command.id, existing_education)
