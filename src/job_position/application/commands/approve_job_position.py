from dataclasses import dataclass

from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.command_bus import Command


@dataclass
class ActivateJobPositionCommand(Command):
    id: JobPositionId


class ActivateJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: ActivateJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.activate()

        self.job_position_repository.save(job_position)


@dataclass
class PauseJobPositionCommand(Command):
    id: JobPositionId


class PauseJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: PauseJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.pause()
        self.job_position_repository.save(job_position)


@dataclass
class ResumeJobPositionCommand(Command):
    id: JobPositionId


class ResumeJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: ResumeJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.resume()
        self.job_position_repository.save(job_position)


@dataclass
class CloseJobPositionCommand(Command):
    id: JobPositionId


class CloseJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: CloseJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.close()

        self.job_position_repository.save(job_position)


@dataclass
class ArchiveJobPositionCommand(Command):
    id: JobPositionId


class ArchiveJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: ArchiveJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.archive()

        self.job_position_repository.save(job_position)
