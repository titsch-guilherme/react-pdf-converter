"""PDF conversion service with job management."""

import asyncio
import os
import uuid
from datetime import datetime
from pathlib import Path

from fastapi import UploadFile
from loguru import logger

from app.core.config import settings
from app.schemas.status import JobStatus
from app.utils.file_handler import FileHandler


class ConversionJob:
    """Represents a single PDF conversion job."""

    def __init__(
        self, job_id: str, filename: str, user_id: str, session_id: str, file_path: str
    ):
        self.job_id = job_id
        self.filename = filename
        self.user_id = user_id
        self.session_id = session_id
        self.file_path = file_path
        self.status = "queued"
        self.progress = 0
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
        self.download_url: str | None = None
        self.error: str | None = None
        self.output_path: str | None = None

    def update_status(self, status: str, progress: int = None, error: str = None):
        """Update job status and timestamp."""
        self.status = status
        if progress is not None:
            self.progress = progress
        if error is not None:
            self.error = error
        self.updated_at = datetime.utcnow()

        logger.info(
            f"Job {self.job_id} status updated to {status}",
            extra={
                "job_id": self.job_id,
                "status": status,
                "progress": progress,
                "user_id": self.user_id,
            },
        )

    def to_status(self) -> JobStatus:
        """Convert to JobStatus schema."""
        return JobStatus(
            job_id=self.job_id,
            filename=self.filename,
            status=self.status,
            progress=self.progress,
            created_at=self.created_at,
            updated_at=self.updated_at,
            download_url=self.download_url,
            error=self.error,
        )


class ConversionService:
    """Service for managing PDF conversion jobs."""

    def __init__(self):
        self.jobs: dict[str, ConversionJob] = {}
        self.user_jobs: dict[str, list[str]] = {}  # user_id -> list of job_ids
        self.file_handler = FileHandler()

        # Ensure directories exist
        self._ensure_directories()

    def _ensure_directories(self):
        """Ensure upload and processed directories exist."""
        Path(settings.UPLOAD_DIR).mkdir(parents=True, exist_ok=True)
        Path(settings.PROCESSED_DIR).mkdir(parents=True, exist_ok=True)

    async def start_conversion(
        self, file: UploadFile, user_id: str, session_id: str
    ) -> str:
        """Start a new conversion job."""
        # Generate unique job ID
        job_id = str(uuid.uuid4())

        try:
            # Save uploaded file
            file_path = await self.file_handler.save_upload(file, job_id)

            # Create job
            job = ConversionJob(
                job_id=job_id,
                filename=file.filename,
                user_id=user_id,
                session_id=session_id,
                file_path=file_path,
            )

            # Store job
            self.jobs[job_id] = job

            # Add to user's job list
            if user_id not in self.user_jobs:
                self.user_jobs[user_id] = []
            self.user_jobs[user_id].append(job_id)

            # Start background processing
            asyncio.create_task(self._process_job(job))

            logger.info(
                f"Conversion job created: {job_id}",
                extra={"job_id": job_id, "filename": file.filename, "user_id": user_id},
            )

            return job_id

        except Exception as e:
            logger.error(f"Failed to start conversion job: {e}")
            raise

    async def _process_job(self, job: ConversionJob):
        """Process a conversion job in the background."""
        try:
            # Update status to processing
            job.update_status("processing", progress=10)

            # Simulate OCR processing (replace with actual OCR implementation)
            await self._simulate_ocr_processing(job)

            # Mark as completed
            job.update_status("completed", progress=100)
            job.download_url = f"/api/v1/download/{job.job_id}"

            logger.info(
                f"Conversion job completed: {job.job_id}",
                extra={"job_id": job.job_id, "user_id": job.user_id},
            )

        except Exception as e:
            logger.error(
                f"Conversion job failed: {job.job_id} - {e}",
                extra={"job_id": job.job_id, "user_id": job.user_id},
            )
            job.update_status("failed", error=str(e))

    async def _simulate_ocr_processing(self, job: ConversionJob):
        """
        Simulate OCR processing with progress updates.

        In a real implementation, this would:
        1. Convert PDF pages to images using pdf2image
        2. Run OCR on each image using pytesseract
        3. Create a new searchable PDF using reportlab
        4. Save the result to the processed directory
        """
        # Simulate processing steps with delays
        steps = [
            ("Converting PDF to images", 30),
            ("Running OCR on pages", 60),
            ("Creating searchable PDF", 80),
            ("Finalizing output", 95),
        ]

        for step_name, progress in steps:
            await asyncio.sleep(1)  # Simulate processing time
            job.update_status("processing", progress=progress)

            logger.debug(
                f"Job {job.job_id}: {step_name}",
                extra={"job_id": job.job_id, "step": step_name, "progress": progress},
            )

        # Create output file path
        output_filename = f"{job.job_id}_searchable.pdf"
        output_path = os.path.join(settings.PROCESSED_DIR, output_filename)

        # Simulate creating the output file (copy input for now)
        import shutil

        shutil.copy2(job.file_path, output_path)

        job.output_path = output_path

    async def get_job_status(self, job_id: str, user_id: str) -> JobStatus | None:
        """Get status of a specific job."""
        job = self.jobs.get(job_id)

        if not job or job.user_id != user_id:
            return None

        return job.to_status()

    async def get_user_jobs(self, user_id: str) -> list[JobStatus]:
        """Get all jobs for a specific user."""
        job_ids = self.user_jobs.get(user_id, [])
        jobs = []

        for job_id in job_ids:
            job = self.jobs.get(job_id)
            if job:
                jobs.append(job.to_status())

        # Sort by creation time (newest first)
        jobs.sort(key=lambda x: x.created_at, reverse=True)

        return jobs

    async def get_download_file_path(self, job_id: str) -> str | None:
        """Get the file path for downloading a completed job."""
        job = self.jobs.get(job_id)

        if not job or job.status != "completed" or not job.output_path:
            return None

        return job.output_path

    def cleanup_old_jobs(self, max_age_hours: int = 24):
        """Clean up old jobs and their files."""
        from datetime import timedelta

        cutoff_time = datetime.utcnow() - timedelta(hours=max_age_hours)
        jobs_to_remove = []

        for job_id, job in self.jobs.items():
            if job.created_at < cutoff_time:
                jobs_to_remove.append(job_id)

                # Clean up files
                try:
                    if os.path.exists(job.file_path):
                        os.remove(job.file_path)
                    if job.output_path and os.path.exists(job.output_path):
                        os.remove(job.output_path)
                except Exception as e:
                    logger.error(f"Error cleaning up files for job {job_id}: {e}")

        # Remove jobs from memory
        for job_id in jobs_to_remove:
            job = self.jobs.pop(job_id, None)
            if job:
                # Remove from user's job list
                user_job_list = self.user_jobs.get(job.user_id, [])
                if job_id in user_job_list:
                    user_job_list.remove(job_id)

        if jobs_to_remove:
            logger.info(f"Cleaned up {len(jobs_to_remove)} old jobs")

        return len(jobs_to_remove)


# Global service instance
conversion_service = ConversionService()
