from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.candidate.domain.entities import CandidateEducation
from src.candidate.domain.repositories.candidate_education_repository_interface import \
    CandidateEducationRepositoryInterface
from src.candidate.domain.value_objects.candidate_education_id import CandidateEducationId
from src.candidate.domain.value_objects.candidate_id import CandidateId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class CreateEducationCommand(Command):
    id: CandidateEducationId
    candidate_id: CandidateId
    degree: str
    institution: str
    description: str
    start_date: date
    end_date: Optional[date]


class CreateEducationCommandHandler(CommandHandler[CreateEducationCommand]):
    def __init__(self, education_repository: CandidateEducationRepositoryInterface):
        self.education_repository = education_repository

    def execute(self, command: CreateEducationCommand) -> None:
        if command.end_date is not None and command.end_date < command.start_date:
            raise ValueError("End date cannot be before start date")

        new_education = CandidateEducation(
            id=command.id,
            candidate_id=command.candidate_id,
            degree=command.degree,
            institution=command.institution,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date,
        )

        self.education_repository.create(new_education)
    # self.event_bus.dispatch(CandidateEducationCreatedEvent.create(id=command.id))
