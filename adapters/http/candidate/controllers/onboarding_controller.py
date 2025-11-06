import logging
import threading
from typing import Optional

from fastapi import UploadFile, HTTPException
from pydantic import ValidationError

from adapters.http.candidate.schemas.onboarding import LandingRequest, LandingResponse
from core.database import database
from src.shared.application.command_bus import CommandBus
from src.shared.application.query_bus import QueryBus
from src.shared.domain.entities.async_job import AsyncJobId
from src.shared.domain.entities.base import generate_id
from src.shared.domain.enums.async_job import AsyncJobType, AsyncJobStatus
from src.shared.infrastructure.jobs.async_job_service import AsyncJobService
from src.shared.infrastructure.repositories.async_job_repository import AsyncJobRepository
from src.shared.infrastructure.services.ai.ai_service_factory import get_ai_service
from src.user.application.commands.create_user_from_landing import CreateUserFromLandingCommand
from src.user.application.queries.create_access_token_query import CreateAccessTokenQuery
from src.user.application.queries.dtos.auth_dto import TokenDto


class OnboardingController:
    """Controlador para el proceso de onboarding de candidatos"""

    def __init__(self, command_bus: CommandBus, query_bus: QueryBus):
        self.command_bus = command_bus
        self.query_bus = query_bus
        self.logger = logging.getLogger(__name__)

    async def process_landing(
            self,
            email: str,
            job_position_id: Optional[str] = None,
            resume_file: Optional[UploadFile] = None
    ) -> LandingResponse:
        """Procesar formulario de landing page"""
        try:
            # Validate input
            try:
                request_data = LandingRequest(
                    email=email,
                    job_position_id=job_position_id
                )
            except ValidationError as e:
                raise HTTPException(status_code=400, detail=f"Invalid input: {str(e)}")

            # Process PDF file if provided
            pdf_bytes = None
            pdf_filename = None
            if resume_file:
                # Validate file type
                if not resume_file.content_type == "application/pdf":
                    raise HTTPException(status_code=400, detail="Only PDF files are allowed")

                # Read file content
                pdf_bytes = await resume_file.read()
                pdf_filename = resume_file.filename

                # Validate file size (max 10MB)
                if len(pdf_bytes) > 10 * 1024 * 1024:
                    raise HTTPException(status_code=400, detail="File size too large (max 10MB)")

            # Create command
            command = CreateUserFromLandingCommand(
                email=request_data.email,
                pdf_file=pdf_bytes,
                pdf_filename=pdf_filename,
                job_position_id=request_data.job_position_id
            )

            # Execute command
            self.command_bus.dispatch(command)

            # Start PDF analysis if PDF was uploaded
            analysis_job_id = None
            if command.user_asset_id and command.candidate_id:
                analysis_job_id = self._start_pdf_analysis(command.user_asset_id, command.candidate_id)

            # Generate JWT token for the user
            access_token = None
            try:
                token_data = {"sub": request_data.email}
                token_query = CreateAccessTokenQuery(data=token_data)
                token_dto: TokenDto = self.query_bus.query(token_query)
                access_token = token_dto.access_token
                self.logger.info(f"Generated access token for user {request_data.email}")
            except Exception as token_error:
                self.logger.warning(f"Could not generate token for user {request_data.email}: {str(token_error)}")

            # Return success response with redirect URL
            return LandingResponse(
                success=True,
                message="",
                user_created=True,
                candidate_created=True,
                application_created=bool(job_position_id),
                access_token=access_token,
                analysis_job_id=analysis_job_id,
                redirect_url="/candidate/onboarding/complete-profile"
            )

        except HTTPException:
            # Re-raise HTTP exceptions
            raise
        except Exception as e:
            self.logger.error(f"Error processing landing: {str(e)}")
            raise HTTPException(
                status_code=500,
                detail="Error interno del servidor. Por favor, intenta de nuevo."
            )

    def _start_pdf_analysis(self, user_asset_id: str, candidate_id: str) -> Optional[str]:
        """Start PDF analysis and return job ID - WORKAROUND: Direct AI analysis"""
        try:
            # Generate job ID
            job_id = AsyncJobId(generate_id())

            # WORKAROUND: Use direct AI analysis instead of broken queue system
            self.logger.info(
                f"Starting direct AI analysis (workaround) for candidate {candidate_id} and asset {user_asset_id}")

            # 1. Create async job in database
            repository = AsyncJobRepository(database)
            async_job_service = AsyncJobService(repository)

            async_job_service.create_job(
                id=job_id,
                job_type=AsyncJobType.PDF_ANALYSIS,
                entity_type="user_asset",
                entity_id=user_asset_id,
                metadata={
                    "candidate_id": candidate_id,
                    "started_by": "direct_analysis_workaround",
                    "asset_type": "pdf_resume"
                },
                timeout_seconds=90
            )

            # 2. Start direct AI analysis in background thread (non-blocking)
            analysis_thread = threading.Thread(
                target=self._process_pdf_directly,
                args=(str(job_id), user_asset_id, candidate_id, async_job_service),
                daemon=True  # Allow main process to exit even if thread is running
            )
            analysis_thread.start()
            self.logger.info(f"Started background PDF analysis thread for job {job_id}")

            self.logger.info(
                f"Started direct PDF analysis job {job_id} for candidate {candidate_id} and asset {user_asset_id}")
            return str(job_id)

        except Exception as e:
            self.logger.error(f"Failed to start PDF analysis: {str(e)}")
            return None

    def _process_pdf_directly(self, job_id: str, user_asset_id: str, candidate_id: str,
                              async_job_service: AsyncJobService) -> None:
        """Process PDF directly with AI - workaround for queue issues"""
        try:
            # Update job status to processing
            async_job_service.update_job_status(
                job_id=job_id,
                status=AsyncJobStatus.PROCESSING,
                progress=10,
                message="Analizando PDF con IA..."
            )

            # Get PDF content from database
            from sqlalchemy import text
            with database.get_session() as session:
                result = session.execute(
                    text("SELECT text_content FROM user_assets WHERE id = :asset_id"),
                    {"asset_id": user_asset_id}
                ).fetchone()

                if not result or not result[0]:
                    raise ValueError(f"No text content found for asset {user_asset_id}")

                text_content = str(result[0])

            # Analyze with AI (automatically uses xAI or Groq based on configuration)
            ai_service = get_ai_service()
            analysis_result = ai_service.analyze_resume_pdf(text_content)

            if analysis_result.success:
                # Complete job with analysis results
                results = {
                    "analysis_successful": True,
                    "candidate_info": analysis_result.candidate_info,
                    "experiences": analysis_result.experiences,
                    "educations": analysis_result.educations,
                    "projects": analysis_result.projects,
                    "skills": analysis_result.skills,
                    "confidence_score": analysis_result.confidence_score,
                    "raw_response": analysis_result.raw_response,
                    "user_asset_id": user_asset_id,
                    "candidate_id": candidate_id
                }

                # Populate candidate profile with extracted data
                try:
                    self._populate_candidate_from_analysis(candidate_id, results)
                    self.logger.info(f"Successfully populated candidate {candidate_id} from PDF analysis")
                except Exception as e:
                    self.logger.error(f"Failed to populate candidate {candidate_id}: {str(e)}")
                    # Don't fail the job if population fails - just log the error

                async_job_service.complete_job(job_id, results)
                self.logger.info(f"Direct AI analysis completed successfully for job {job_id}")
            else:
                async_job_service.fail_job(job_id, f"AI analysis failed: {analysis_result.error_message}")

        except Exception as e:
            self.logger.error(f"Direct PDF analysis failed for job {job_id}: {str(e)}")
            try:
                async_job_service.fail_job(job_id, f"Direct analysis error: {str(e)}")
            except Exception:
                pass  # Don't fail if we can't update status

    def _populate_candidate_from_analysis(self, candidate_id: str, analysis_results: dict) -> None:
        """Populate candidate profile from PDF analysis results."""
        try:
            from src.candidate.application.commands.populate_candidate_from_pdf_analysis import (
                PopulateCandidateFromPdfAnalysisCommand
            )

            # Create and execute the populate command
            populate_command = PopulateCandidateFromPdfAnalysisCommand(
                candidate_id=candidate_id,
                analysis_results=analysis_results
            )

            self.command_bus.dispatch(populate_command)
            self.logger.info(f"Candidate {candidate_id} populated from PDF analysis results")

        except Exception as e:
            self.logger.error(f"Error populating candidate from analysis: {str(e)}")
            raise
