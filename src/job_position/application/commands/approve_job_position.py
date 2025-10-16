from dataclasses import dataclass
from typing import Optional

from src.job_position.domain.exceptions import JobPositionNotFoundException
from src.job_position.domain.value_objects import JobPositionId
from src.job_position.infrastructure.repositories.job_position_repository import JobPositionRepositoryInterface
from src.shared.application.command_bus import Command


@dataclass
class ApproveJobPositionCommand(Command):
    id: JobPositionId
    approved_by: str
    approval_notes: Optional[str] = None


class ApproveJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: ApproveJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.approve()

        self.job_position_repository.save(job_position)


@dataclass
class RejectJobPositionCommand(Command):
    id: JobPositionId


class RejectJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: RejectJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.reject(
        )

        self.job_position_repository.save(job_position)


@dataclass
class OpenJobPositionCommand(Command):
    id: JobPositionId


class OpenJobPositionCommandHandler:
    def __init__(self, job_position_repository: JobPositionRepositoryInterface):
        self.job_position_repository = job_position_repository

    def execute(self, command: OpenJobPositionCommand) -> None:
        job_position = self.job_position_repository.get_by_id(command.id)
        if not job_position:
            raise JobPositionNotFoundException(f"Job position with id {command.id.value} not found")

        job_position.open_position()

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

        job_position.close_position(
        )

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

        job_position.pause_position(
        )
        self.job_position_repository.save(job_position)
