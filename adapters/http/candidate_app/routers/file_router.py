import logging
from typing import Annotated, Any, Dict

from dependency_injector.wiring import inject, Provide
from fastapi import APIRouter, Depends, Header, UploadFile, File, HTTPException

from core.container import Container
from src.framework.application.command_bus import CommandBus
from src.framework.infrastructure.jobs.async_job_service import AsyncJobService

logger = logging.getLogger(__name__)

file_router = APIRouter(prefix="/api/files", tags=["files"])


@file_router.post("/upload-pdf")
@inject
async def upload_pdf(
        *,
        file: UploadFile = File(...),
        authorization: str = Header(...),
        command_bus: Annotated[CommandBus, Depends(Provide[Container.command_bus])],
) -> None:
    pass


@file_router.get("/analysis-status/{job_id}")
@inject
async def get_analysis_status(
        job_id: str,
        async_job_service: Annotated[AsyncJobService, Depends(Provide[Container.async_job_service])],
) -> Dict[str, Any]:
    """Get PDF analysis job status"""
    try:
        job_status = async_job_service.get_job_status(job_id)

        if not job_status:
            raise HTTPException(status_code=404, detail="Analysis job not found")

        return job_status

    except Exception as e:
        logger.error(f"Error getting analysis status for job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analysis status")


@file_router.get("/analysis-results/{job_id}")
@inject
async def get_analysis_results(
        job_id: str,
        async_job_service: Annotated[AsyncJobService, Depends(Provide[Container.async_job_service])],
) -> Dict[str, Any]:
    """Get PDF analysis job results if completed"""
    try:
        job_results = async_job_service.get_job_results(job_id)

        if not job_results:
            raise HTTPException(status_code=404, detail="Analysis results not found or job not completed")

        return job_results

    except Exception as e:
        logger.error(f"Error getting analysis results for job {job_id}: {e}")
        raise HTTPException(status_code=500, detail="Failed to get analysis results")
