"""Direct AI testing router - no queues."""

import logging
from typing import Dict, Any
from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import JSONResponse

from core.config import settings
from src.framework.infrastructure.services.ai.ai_service_factory import get_ai_service
from src.auth_bc.user.infrastructure.services.pdf_processing_service import PDFProcessingService

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/test", tags=["AI Testing"])


@router.post("/analyze-pdf-direct")
async def analyze_pdf_direct(file: UploadFile = File(...)) -> JSONResponse:
    """
    Direct PDF analysis with AI (xAI or Groq based on configuration) - no queues, immediate response.

    This endpoint is for testing purposes only.
    """
    if not file.filename or not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="Only PDF files are allowed")

    try:
        logger.info(f"Starting direct AI analysis for file: {file.filename or 'unknown'}")

        # 1. Read PDF content
        pdf_content = await file.read()
        logger.info(f"PDF file size: {len(pdf_content)} bytes")

        # 2. Extract text from PDF
        pdf_service = PDFProcessingService()
        extraction_result = pdf_service.extract_text_from_pdf(pdf_content)

        if extraction_result["status"] != "completed" or not extraction_result["text"]:
            error_msg = extraction_result.get("error", "Unknown extraction error")
            raise HTTPException(
                status_code=400,
                detail=f"Could not extract text from PDF: {error_msg}"
            )

        text_content = extraction_result["text"]

        if len(text_content.strip()) < 50:
            raise HTTPException(
                status_code=400,
                detail=f"PDF text too short for analysis. Extracted: {len(text_content)} characters"
            )

        logger.info(f"Extracted text length: {len(text_content)} characters")
        logger.info(f"Text preview: {text_content[:200]}...")
        logger.info(f"PDF metadata: {extraction_result.get('metadata', {})}")

        # 3. Analyze with AI (automatically uses xAI or Groq based on configuration)
        ai_service = get_ai_service()
        analysis_result = ai_service.analyze_resume_pdf(text_content)

        # 4. Return results
        response_data = {
            "success": analysis_result.success,
            "filename": file.filename or "unknown",
            "text_length": len(text_content),
            "text_preview": text_content[:500] + "..." if len(text_content) > 500 else text_content,
            "analysis_result": {
                "candidate_info": analysis_result.candidate_info,
                "experiences": analysis_result.experiences,
                "educations": analysis_result.educations,
                "projects": analysis_result.projects,
                "skills": analysis_result.skills,
                "confidence_score": analysis_result.confidence_score,
            },
            "raw_ai_response": analysis_result.raw_response,
            "error_message": analysis_result.error_message
        }

        logger.info(f"Analysis completed successfully. Confidence: {analysis_result.confidence_score}")
        return JSONResponse(content=response_data)

    except Exception as e:
        logger.error(f"Direct AI analysis failed: {str(e)}")
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e),
                "filename": file.filename or "unknown"
            }
        )


@router.get("/ai-config")
async def get_ai_config() -> Dict[str, Any]:
    """Get current AI configuration for debugging."""
    try:
        ai_service = get_ai_service()
        # Use getattr to safely access implementation-specific attributes
        api_key = getattr(ai_service, 'api_key', None)
        return {
            "ai_agent": settings.AI_AGENT,
            "model": getattr(ai_service, 'model', 'unknown'),
            "max_tokens": getattr(ai_service, 'max_tokens', None),
            "timeout": getattr(ai_service, 'timeout', None),
            "api_url": getattr(ai_service, 'api_url', 'unknown'),
            "has_api_key": bool(api_key),
            "api_key_preview": f"{api_key[:10]}..." if api_key else None
        }
    except Exception as e:
        return {"error": str(e)}
