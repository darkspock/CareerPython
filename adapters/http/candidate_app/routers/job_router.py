import logging
from typing import Annotated, Any, Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, HTTPException

from core.containers import Container
from src.framework.infrastructure.jobs.async_job_service import AsyncJobService

logger = logging.getLogger(__name__)

job_router = APIRouter(prefix="/api/jobs", tags=["jobs"])


@job_router.get("/{job_id}/status")
@inject
async def get_job_status(
        job_id: str,
        async_job_service: Annotated[AsyncJobService, Depends(Provide[Container.async_job_service])],
) -> Dict[str, Any]:
    """Get job status for frontend polling - supports PDF analysis and other async jobs"""
    try:
        job_status = async_job_service.get_job_status(job_id)

        if not job_status:
            raise HTTPException(status_code=404, detail="Job not found")

        # Format response for frontend polling
        return {
            "job_id": job_id,
            "status": job_status.get("status", "unknown"),
            "progress": job_status.get("progress", 0),
            "message": job_status.get("message", ""),
            "completed_at": job_status.get("completed_at"),
            "error_message": job_status.get("error_message"),
            "results": job_status.get("results") if job_status.get("status") == "completed" else None
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status for {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get job status")


@job_router.get("/{job_id}/results")
@inject
async def get_job_results(
        job_id: str,
        async_job_service: Annotated[AsyncJobService, Depends(Provide[Container.async_job_service])],
) -> Dict[str, Any]:
    """Get job results if completed - alias for better API consistency"""
    try:
        job_results = async_job_service.get_job_results(job_id)

        if not job_results:
            raise HTTPException(status_code=404, detail="Job results not found or job not completed")

        return job_results

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job results for {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get job results")
