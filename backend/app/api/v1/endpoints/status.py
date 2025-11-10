"""Job status endpoints."""

from fastapi import APIRouter, Depends, HTTPException, status
from loguru import logger

from app.core.dependencies import get_current_user
from app.schemas.status import BatchStatusResponse, JobStatus
from app.services.conversion import conversion_service

router = APIRouter()


@router.get("/{job_id}", response_model=JobStatus)
async def get_job_status(job_id: str, current_user: dict = Depends(get_current_user)):
    """
    Get status of a specific conversion job.

    Returns the current status, progress, and any error information
    for the specified job ID.
    """
    try:
        job_status = await conversion_service.get_job_status(
            job_id=job_id, user_id=current_user["user_id"]
        )

        if not job_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found or access denied",
            )

        return job_status

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error getting job status for {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Status service temporarily unavailable",
        )


@router.get("", response_model=BatchStatusResponse)
async def get_all_jobs_status(current_user: dict = Depends(get_current_user)):
    """
    Get status of all conversion jobs for the current user.

    Returns a list of all jobs (active and completed) for the current user
    with their current status and progress information.
    """
    try:
        jobs = await conversion_service.get_user_jobs(user_id=current_user["user_id"])

        return BatchStatusResponse(jobs=jobs)

    except Exception as e:
        logger.error(f"Error getting user jobs: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Status service temporarily unavailable",
        )
