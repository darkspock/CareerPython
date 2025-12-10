"""
Job Position Status Transition Commands

These commands handle the publishing flow state machine transitions:
- RequestApprovalCommand: DRAFT -> PENDING_APPROVAL
- ApproveCommand: PENDING_APPROVAL -> APPROVED
- RejectCommand: PENDING_APPROVAL -> REJECTED
- PublishCommand: APPROVED/DRAFT -> PUBLISHED
- HoldCommand: PUBLISHED -> ON_HOLD
- ResumeCommand: ON_HOLD -> PUBLISHED
- CloseCommand: PUBLISHED/ON_HOLD -> CLOSED
- ArchiveCommand: various -> ARCHIVED
- CloneCommand: Create copy in DRAFT
"""
from dataclasses import dataclass
from typing import Optional

from src.company_bc.company.domain.value_objects.company_user_id import CompanyUserId
from src.company_bc.job_position.domain.entities.job_position import JobPosition
from src.company_bc.job_position.domain.enums import ClosedReasonEnum
from src.company_bc.job_position.domain.exceptions.job_position_exceptions import (
    JobPositionNotFoundException,
)
from src.company_bc.job_position.domain.repositories.job_position_repository_interface import (
    JobPositionRepositoryInterface,
)
from src.company_bc.job_position.domain.value_objects import JobPositionId
from src.framework.application.command_bus import Command, CommandHandler


# ==================== REQUEST APPROVAL ====================

@dataclass
class RequestJobPositionApprovalCommand(Command):
    """Command to request approval for a job position (DRAFT -> PENDING_APPROVAL)"""
    job_position_id: str
    company_id: str


class RequestJobPositionApprovalCommandHandler(CommandHandler[RequestJobPositionApprovalCommand]):
    """Handler for RequestJobPositionApprovalCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: RequestJobPositionApprovalCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        # Validate salary against budget before requesting approval
        job_position.validate_salary_against_budget()

        # Request approval (validates required fields and transitions status)
        job_position.request_approval()

        self.repository.save(job_position)


# ==================== APPROVE ====================

@dataclass
class ApproveJobPositionCommand(Command):
    """Command to approve a job position (PENDING_APPROVAL -> APPROVED)"""
    job_position_id: str
    approver_id: str  # CompanyUserId of the approver
    company_id: str


class ApproveJobPositionCommandHandler(CommandHandler[ApproveJobPositionCommand]):
    """Handler for ApproveJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: ApproveJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        approver_id = CompanyUserId.from_string(command.approver_id)
        job_position.approve(approver_id)

        self.repository.save(job_position)


# ==================== REJECT ====================

@dataclass
class RejectJobPositionCommand(Command):
    """Command to reject a job position (PENDING_APPROVAL -> REJECTED)"""
    job_position_id: str
    company_id: str
    reason: Optional[str] = None


class RejectJobPositionCommandHandler(CommandHandler[RejectJobPositionCommand]):
    """Handler for RejectJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: RejectJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        job_position.reject(command.reason)

        self.repository.save(job_position)


# ==================== PUBLISH ====================

@dataclass
class PublishJobPositionCommand(Command):
    """Command to publish a job position (APPROVED/DRAFT -> PUBLISHED)"""
    job_position_id: str
    company_id: str


class PublishJobPositionCommandHandler(CommandHandler[PublishJobPositionCommand]):
    """Handler for PublishJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: PublishJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        # Freeze custom fields on publish
        job_position.freeze_custom_fields()

        # Publish (sets visibility to PUBLIC, sets published_at)
        job_position.publish()

        self.repository.save(job_position)


# ==================== HOLD ====================

@dataclass
class HoldJobPositionCommand(Command):
    """Command to put a job position on hold (PUBLISHED -> ON_HOLD)"""
    job_position_id: str
    company_id: str


class HoldJobPositionCommandHandler(CommandHandler[HoldJobPositionCommand]):
    """Handler for HoldJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: HoldJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        job_position.put_on_hold()

        self.repository.save(job_position)


# ==================== RESUME ====================

@dataclass
class ResumeJobPositionCommand(Command):
    """Command to resume a held job position (ON_HOLD -> PUBLISHED)"""
    job_position_id: str
    company_id: str


class ResumeJobPositionCommandHandler(CommandHandler[ResumeJobPositionCommand]):
    """Handler for ResumeJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: ResumeJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        job_position.resume()

        self.repository.save(job_position)


# ==================== CLOSE ====================

@dataclass
class CloseJobPositionCommand(Command):
    """Command to close a job position (PUBLISHED/ON_HOLD -> CLOSED)"""
    job_position_id: str
    company_id: str
    closed_reason: str  # ClosedReasonEnum value


class CloseJobPositionCommandHandler(CommandHandler[CloseJobPositionCommand]):
    """Handler for CloseJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: CloseJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        reason = ClosedReasonEnum(command.closed_reason)
        job_position.close(reason)

        self.repository.save(job_position)


# ==================== ARCHIVE ====================

@dataclass
class ArchiveJobPositionCommand(Command):
    """Command to archive a job position (various -> ARCHIVED)"""
    job_position_id: str
    company_id: str


class ArchiveJobPositionCommandHandler(CommandHandler[ArchiveJobPositionCommand]):
    """Handler for ArchiveJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: ArchiveJobPositionCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        job_position.archive()

        self.repository.save(job_position)


# ==================== REVERT TO DRAFT ====================

@dataclass
class RevertJobPositionToDraftCommand(Command):
    """Command to revert a job position to draft (REJECTED/APPROVED/CLOSED -> DRAFT)"""
    job_position_id: str
    company_id: str


class RevertJobPositionToDraftCommandHandler(CommandHandler[RevertJobPositionToDraftCommand]):
    """Handler for RevertJobPositionToDraftCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: RevertJobPositionToDraftCommand) -> None:
        job_position = self.repository.get_by_id(
            JobPositionId.from_string(command.job_position_id)
        )
        if not job_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.job_position_id} not found"
            )

        job_position.revert_to_draft()

        self.repository.save(job_position)


# ==================== CLONE ====================

@dataclass
class CloneJobPositionCommand(Command):
    """Command to clone a job position (creates new position in DRAFT)"""
    source_job_position_id: str
    company_id: str
    new_job_position_id: str  # Pre-generated ID for the new position


class CloneJobPositionCommandHandler(CommandHandler[CloneJobPositionCommand]):
    """Handler for CloneJobPositionCommand"""

    def __init__(self, repository: JobPositionRepositoryInterface):
        self.repository = repository

    def execute(self, command: CloneJobPositionCommand) -> None:
        source_position = self.repository.get_by_id(
            JobPositionId.from_string(command.source_job_position_id)
        )
        if not source_position:
            raise JobPositionNotFoundException(
                f"Job position with id {command.source_job_position_id} not found"
            )

        new_id = JobPositionId.from_string(command.new_job_position_id)
        cloned_position = source_position.clone(new_id)

        self.repository.save(cloned_position)
