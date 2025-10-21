"""Dramatiq actor for PDF resume analysis."""

import logging
from typing import Dict, Any, Optional

import dramatiq

from core.database import database
from ..jobs.async_job_service import AsyncJobService
from ..repositories.async_job_repository import AsyncJobRepository
from ..services.ai.ai_service_factory import get_ai_service
from ...domain.enums.async_job import AsyncJobStatus

logger = logging.getLogger(__name__)


@dramatiq.actor  # Simplified actor without retries to avoid middleware issues
def analyze_pdf_resume(job_id: str, user_asset_id: str, candidate_id: str) -> None:
    """
    Analyze PDF resume using AI (xAI or Groq based on configuration) and populate candidate data.

    Args:
        job_id: ID of the async job
        user_asset_id: ID of the user asset containing the PDF
        candidate_id: ID of the candidate to populate
    """
    logger.info(f"Starting PDF analysis for job {job_id}, asset {user_asset_id}, candidate {candidate_id}")

    # Initialize services
    repository = AsyncJobRepository(database)
    async_job_service = AsyncJobService(repository)

    # Get AI service (automatically selects xAI or Groq based on configuration)
    ai_service = get_ai_service()

    try:
        # 1. Update progress: Starting analysis
        async_job_service.update_job_status(
            job_id=job_id,
            status=AsyncJobStatus.PROCESSING,
            progress=10,
            message="Obteniendo contenido del PDF..."
        )

        # 2. Get PDF content
        pdf_content = _get_user_asset_content(user_asset_id)
        if not pdf_content:
            raise ValueError(f"No se pudo obtener el contenido del PDF {user_asset_id}")

        logger.info(f"Retrieved PDF content for asset {user_asset_id}, length: {len(pdf_content)}")

        # 3. Update progress: Analyzing with AI
        async_job_service.update_job_status(
            job_id=job_id,
            status=AsyncJobStatus.PROCESSING,
            progress=50,
            message="Analizando CV con IA..."
        )

        # 4. Analyze with AI
        ai_result = ai_service.analyze_resume_pdf(pdf_content)

        if not ai_result.success:
            raise ValueError(f"AI analysis failed: {ai_result.error_message}")

        # Validate result quality
        if not ai_service.validate_analysis_result(ai_result):
            logger.warning(f"Low quality analysis result for job {job_id}")
            # Continue anyway but with lower confidence

        logger.info(f"AI analysis completed with confidence: {ai_result.confidence_score}")

        # 5. Update progress: Populating candidate data
        async_job_service.update_job_status(
            job_id=job_id,
            status=AsyncJobStatus.PROCESSING,
            progress=80,
            message="Poblando perfil del candidato..."
        )

        # 6. Populate candidate data from analysis results
        results = {
            "analysis_successful": True,
            "candidate_info": ai_result.candidate_info,
            "experiences": ai_result.experiences,
            "educations": ai_result.educations,
            "projects": ai_result.projects,
            "skills": ai_result.skills,
            "confidence_score": ai_result.confidence_score,
            "raw_response": ai_result.raw_response,
            "user_asset_id": user_asset_id,
            "candidate_id": candidate_id
        }

        # Populate candidate profile with extracted data
        try:
            _populate_candidate_from_analysis(candidate_id, results)
            logger.info(f"Successfully populated candidate {candidate_id} from PDF analysis")
        except Exception as e:
            logger.error(f"Failed to populate candidate {candidate_id}: {str(e)}")
            # Don't fail the job if population fails - just log the error

        # 7. Complete job with analysis results
        async_job_service.complete_job(job_id, results)
        logger.info(f"PDF analysis completed successfully for job {job_id}. Confidence: {ai_result.confidence_score}")

    except Exception as e:
        logger.error(f"PDF analysis failed for job {job_id}: {str(e)}")
        async_job_service.fail_job(job_id, f"Error en análisis: {str(e)}")
        raise  # Re-raise for Dramatiq retry logic


def _get_user_asset_content(user_asset_id: str) -> Optional[str]:
    """Get text content from user asset using direct database query."""
    try:
        from sqlalchemy import text

        # Use direct SQL query to avoid repository dependencies
        with database.get_session() as session:
            result = session.execute(
                text("SELECT text_content, content FROM user_assets WHERE id = :asset_id"),
                {"asset_id": user_asset_id}
            ).fetchone()

            if not result:
                logger.warning(f"User asset {user_asset_id} not found")
                return None

            text_content, content = result

            # Return text_content if available
            if text_content:
                return str(text_content)

            # Fallback to content field if text_content is not available
            if content and isinstance(content, dict) and 'text' in content:
                text_from_content = content['text']
                return str(text_from_content) if text_from_content is not None else None

            return None

    except Exception as e:
        logger.error(f"Failed to get user asset content for {user_asset_id}: {e}")
        return None


def _populate_candidate_from_analysis(candidate_id: str, analysis_results: Dict[str, Any]) -> None:
    """Populate candidate profile from PDF analysis results."""
    try:
        from src.candidate.application.commands.populate_candidate_from_pdf_analysis import (
            PopulateCandidateFromPdfAnalysisCommand
        )

        # Lazy import to avoid circular dependency
        def get_command_bus() -> Any:
            from core.container import Container
            container = Container()
            return container.command_bus()

        command_bus = get_command_bus()

        # Create and execute the populate command
        populate_command = PopulateCandidateFromPdfAnalysisCommand(
            candidate_id=candidate_id,
            analysis_results=analysis_results
        )

        command_bus.execute(populate_command)
        logger.info(f"Candidate {candidate_id} populated from PDF analysis results")

    except Exception as e:
        logger.error(f"Error populating candidate from analysis: {str(e)}")
        raise
