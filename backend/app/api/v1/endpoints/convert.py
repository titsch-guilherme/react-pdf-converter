"""PDF conversion endpoints."""

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from loguru import logger

from app.core.dependencies import check_rate_limit, get_current_user
from app.schemas.convert import ConversionResponse, JobInfo
from app.services.conversion import conversion_service
from app.utils.validation import validate_pdf_files

router = APIRouter()


@router.post(
    "", response_model=ConversionResponse, dependencies=[Depends(check_rate_limit)]
)
async def convert_pdfs(
    files: list[UploadFile] = File(...), current_user: dict = Depends(get_current_user)
):
    """
    Convert multiple PDF files to searchable PDFs using OCR.

    This endpoint accepts multiple PDF files, validates them, and starts
    background conversion jobs for each file. Returns job IDs for tracking.
    """
    try:
        # Validate files
        validation_result = await validate_pdf_files(files)
        if not validation_result.is_valid:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"File validation failed: {validation_result.error_message}",
            )

        # Start conversion jobs
        jobs = []
        for file in files:
            try:
                job_id = await conversion_service.start_conversion(
                    file=file,
                    user_id=current_user["user_id"],
                    session_id=current_user.get("session_id"),
                )

                jobs.append(
                    JobInfo(
                        job_id=job_id,
                        filename=file.filename or "unknown.pdf",
                        status="queued",
                        error=None,
                    )
                )

                logger.info(
                    f"Started conversion job for file: {file.filename}",
                    extra={
                        "job_id": job_id,
                        "user_id": current_user["user_id"],
                        "filename": file.filename,
                    },
                )

            except Exception as e:
                logger.error(
                    f"Failed to start conversion for file {file.filename}: {e}",
                    extra={
                        "user_id": current_user["user_id"],
                        "filename": file.filename,
                    },
                )

                jobs.append(
                    JobInfo(
                        job_id="",
                        filename=file.filename or "unknown.pdf",
                        status="failed",
                        error=f"Failed to start conversion: {str(e)}",
                    )
                )

        logger.info(
            f"Started {len([j for j in jobs if j.status == 'queued'])} conversion jobs",
            extra={"user_id": current_user["user_id"], "total_files": len(files)},
        )

        return ConversionResponse(jobs=jobs)

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in convert_pdfs endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Conversion service temporarily unavailable",
        )
