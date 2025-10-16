from dataclasses import dataclass
from datetime import date
from typing import Optional

from src.candidate.domain.exceptions import CandidateNotFoundError
from src.candidate.domain.repositories.candidate_project_repository_interface import CandidateProjectRepositoryInterface
from src.candidate.domain.value_objects.candidate_project_id import CandidateProjectId
from src.shared.application.command_bus import Command, CommandHandler


@dataclass
class UpdateProjectCommand(Command):
    id: CandidateProjectId
    name: str
    description: str
    start_date: date
    end_date: Optional[date]


class UpdateProjectCommandHandler(CommandHandler[UpdateProjectCommand]):
    def __init__(self, project_repository: CandidateProjectRepositoryInterface):
        self.project_repository = project_repository

    def execute(self, command: UpdateProjectCommand) -> None:
        existing_project = self.project_repository.get_by_id(command.id)
        if not existing_project:
            raise CandidateNotFoundError("Project not found")
        existing_project.update_details(command.name, command.description, command.start_date, command.end_date)

        self.project_repository.update(command.id, existing_project)
