"""File download endpoints."""

import os

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from loguru import logger

from app.core.dependencies import get_current_user
from app.services.conversion import conversion_service

router = APIRouter()


@router.get("/{job_id}")
async def download_converted_file(
    job_id: str, current_user: dict = Depends(get_current_user)
):
    """
    Download the converted PDF file for a completed job.

    Returns the converted PDF file as a download attachment.
    Only allows download if the job belongs to the current user and is completed.
    """
    try:
        # Get job status to verify ownership and completion
        job_status = await conversion_service.get_job_status(
            job_id=job_id, user_id=current_user["user_id"]
        )

        if not job_status:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Job not found or access denied",
            )

        if job_status.status != "completed":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Job is not completed. Current status: {job_status.status}",
            )

        if not job_status.download_url:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Converted file not found"
            )

        # Get the actual file path
        file_path = await conversion_service.get_download_file_path(job_id)

        if not file_path or not os.path.exists(file_path):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Converted file not found on disk",
            )

        # Generate download filename
        original_filename = job_status.filename
        if original_filename.lower().endswith(".pdf"):
            download_filename = original_filename[:-4] + "_searchable.pdf"
        else:
            download_filename = original_filename + "_searchable.pdf"

        logger.info(
            f"File download started: {download_filename}",
            extra={
                "job_id": job_id,
                "user_id": current_user["user_id"],
                "filename": download_filename,
            },
        )

        return FileResponse(
            path=file_path,
            media_type="application/pdf",
            filename=download_filename,
            headers={
                "Content-Disposition": f"attachment; filename={download_filename}",
                "Cache-Control": "no-cache, no-store, must-revalidate",
                "Pragma": "no-cache",
                "Expires": "0",
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error downloading file for job {job_id}: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Download service temporarily unavailable",
        )
