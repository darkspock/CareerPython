"""Command for analyzing PDF resume asynchronously."""

from dataclasses import dataclass

from src.candidate_bc.candidate.domain.value_objects import CandidateId
from src.framework.application.command_bus import Command, CommandHandler
from src.framework.domain.entities.async_job import AsyncJobId
from src.framework.domain.enums.async_job import AsyncJobType
from src.framework.infrastructure.actors.pdf_analysis_actor import analyze_pdf_resume
from src.framework.infrastructure.jobs.async_job_service import AsyncJobService
from src.auth_bc.user.domain.value_objects.user_asset_id import UserAssetId


@dataclass
class AnalyzePDFResumeCommand(Command):
    """Command to analyze a PDF resume asynchronously."""
    job_id: AsyncJobId
    user_asset_id: UserAssetId
    candidate_id: CandidateId
    timeout_seconds: int = 30


class AnalyzePDFResumeCommandHandler(CommandHandler[AnalyzePDFResumeCommand]):
    """Handler for AnalyzePDFResumeCommand."""

    def __init__(self, async_job_service: AsyncJobService):
        self.async_job_service = async_job_service

    def execute(self, command: AnalyzePDFResumeCommand) -> None:
        """
        Execute the PDF analysis command.

        Creates an async job and processes it immediately (temporary sync mode).
        """
        # 1. Create async job in database
        self.async_job_service.create_job(
            id=command.job_id,
            job_type=AsyncJobType.PDF_ANALYSIS,
            entity_type="user_asset",
            entity_id=str(command.user_asset_id),
            metadata={
                "candidate_id": str(command.candidate_id),
                "started_by": "resume_analysis_command",
                "asset_type": "pdf_resume"
            },
            timeout_seconds=command.timeout_seconds
        )

        # 2. Process asynchronously using Dramatiq
        analyze_pdf_resume.send(
            job_id=command.job_id.value,
            user_asset_id=str(command.user_asset_id),
            candidate_id=str(command.candidate_id)
        )
