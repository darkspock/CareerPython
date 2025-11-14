from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

from src.candidate_bc.candidate.domain.exceptions.candidate_exceptions import ExperienceNotFoundError
from src.candidate_bc.candidate.domain.repositories.candiadate_experience_repository_interface import \
    CandidateExperienceRepositoryInterface
from src.candidate_bc.candidate.domain.value_objects.candidate_experience_id import CandidateExperienceId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class UpdateExperienceCommand(Command):
    id: CandidateExperienceId
    job_title: str
    company: str
    description: str
    start_date: date
    end_date: Optional[date] = None


class UpdateExperienceCommandHandler(CommandHandler[UpdateExperienceCommand]):
    def __init__(self, experience_repository: CandidateExperienceRepositoryInterface):
        self.experience_repository = experience_repository

    def execute(self, command: UpdateExperienceCommand) -> None:
        # Get existing experience
        existing_experience = self.experience_repository.get_by_id(command.id)
        if not existing_experience:
            raise ExperienceNotFoundError(f"Experience with id {command.id.value} not found")

        # Update experience using repository update method
        update_data = {
            'job_title': command.job_title,
            'company': command.company,
            'description': command.description,
            'start_date': command.start_date,
            'end_date': command.end_date,
            'updated_at': datetime.now()
        }

        self.experience_repository.update(command.id, update_data)
