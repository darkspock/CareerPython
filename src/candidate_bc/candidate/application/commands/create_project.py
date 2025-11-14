from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.candidate_bc.candidate.domain.entities import CandidateProject
from src.candidate_bc.candidate.domain.repositories.candidate_project_repository_interface import \
    CandidateProjectRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_id import CandidateId
from src.candidate_bc.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class CreateProjectCommand(Command):
    id: CandidateProjectId
    candidate_id: CandidateId
    name: str
    description: str
    start_date: date
    end_date: Optional[date]


class CreateProjectCommandHandler(CommandHandler[CreateProjectCommand]):
    def __init__(self, project_repository: CandidateProjectRepositoryInterface):
        self.project_repository = project_repository

    def execute(self, command: CreateProjectCommand) -> None:
        if command.end_date is not None and command.end_date < command.start_date:
            raise ValueError("End date cannot be before start date")

        new_project = CandidateProject.create(
            id=command.id,
            candidate_id=command.candidate_id,
            name=command.name,
            description=command.description,
            start_date=command.start_date,
            end_date=command.end_date,
        )

        self.project_repository.create(new_project)
        # self.event_bus.dispatch(CandidateProjectCreatedEvent.create(id=command.id))
