from dataclasses import dataclass

from src.candidate_bc.resume.domain.repositories.resume_repository_interface import ResumeRepositoryInterface
from src.candidate_bc.resume.domain.value_objects.resume_id import ResumeId
from src.framework.application.command_bus import Command, CommandHandler


@dataclass
class DeleteResumeCommand(Command):
    """Command to delete a resume"""
    resume_id: ResumeId


class DeleteResumeCommandHandler(CommandHandler[DeleteResumeCommand]):
    """Handler to delete a resume"""

    def __init__(self, resume_repository: ResumeRepositoryInterface):
        self.resume_repository = resume_repository

    def execute(self, command: DeleteResumeCommand) -> None:
        """Handle the resume deletion command"""

        # 1. Verify that the resume exists
        resume = self.resume_repository.get_by_id(command.resume_id)
        if not resume:
            raise ValueError(f"Resume with id {command.resume_id.value} not found")

        # 2. Verify that it can be deleted
        if not resume.can_be_deleted():
            raise ValueError("Resume cannot be deleted")

        # 3. Delete the resume
        success = self.resume_repository.delete(command.resume_id)
        if not success:
            raise RuntimeError(f"Failed to delete resume {command.resume_id.value}")
