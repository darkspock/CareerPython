from dataclasses import dataclass

from src.company_bc.candidate_application.domain.repositories.candidate_application_repository_interface import \
    CandidateApplicationRepositoryInterface
from src.company_bc.job_position.domain.enums.job_position_visibility import JobPositionVisibilityEnum
from src.company_bc.job_position.domain.exceptions import JobPositionNotFoundException
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.company_bc.job_position.infrastructure.repositories.job_position_repository import \
    JobPositionRepositoryInterface
from src.framework.application.command_bus import Command


@dataclass
class DeleteJobPositionCommand(Command):
    id: JobPositionId


class DeleteJobPositionCommandHandler:
    def __init__(self,
                 job_position_repository: JobPositionRepositoryInterface,
                 candidate_application_repository: CandidateApplicationRepositoryInterface, ):
        self.job_position_repository = job_position_repository
        self.candidate_application_repository = candidate_application_repository

    def execute(self, command: DeleteJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)

        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        candidates = self.candidate_application_repository.get_applications_by_position(command.id)

        if candidates:
            # TODO: Move to a closed stage instead of closing directly
            # For now, we just mark as hidden (not public)
            job_position.visibility = JobPositionVisibilityEnum.HIDDEN
            self.job_position_repository.save(job_position)
        else:
            self.job_position_repository.delete(command.id)
