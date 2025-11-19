"""File handling utilities for upload and processing."""

import os
from pathlib import Path

import aiofiles
from fastapi import UploadFile
from loguru import logger

from app.core.config import settings
from app.utils.validation import sanitize_filename


class FileHandler:
    """Handle file operations for PDF conversion."""

    def __init__(self) -> None:
        self.upload_dir = Path(settings.UPLOAD_DIR)
        self.processed_dir = Path(settings.PROCESSED_DIR)

        # Ensure directories exist
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self.processed_dir.mkdir(parents=True, exist_ok=True)

    async def save_upload(self, file: UploadFile, job_id: str) -> str:
        """
        Save uploaded file to disk with job ID prefix.

        Args:
            file: The uploaded file
            job_id: Unique job identifier

        Returns:
            Path to the saved file
        """
        try:
            # Sanitize filename
            safe_filename = sanitize_filename(file.filename or "unknown.pdf")

            # Create unique filename with job ID
            filename = f"{job_id}_{safe_filename}"
            file_path = self.upload_dir / filename

            # Save file
            async with aiofiles.open(file_path, "wb") as f:
                content = await file.read()
                await f.write(content)

            logger.info(
                f"File saved: {filename}",
                extra={
                    "job_id": job_id,
                    "original_filename": file.filename,
                    "saved_path": str(file_path),
                    "file_size": len(content),
                },
            )

            return str(file_path)

        except Exception as e:
            logger.error(f"Error saving file for job {job_id}: {e}")
            raise

    def get_processed_file_path(self, job_id: str, original_filename: str) -> str:
        """
        Get the path where the processed file should be saved.

        Args:
            job_id: Unique job identifier
            original_filename: Original filename

        Returns:
            Path for the processed file
        """
        safe_filename = sanitize_filename(original_filename)

        # Remove .pdf extension and add _searchable.pdf
        if safe_filename.lower().endswith(".pdf"):
            base_name = safe_filename[:-4]
        else:
            base_name = safe_filename

        processed_filename = f"{job_id}_{base_name}_searchable.pdf"
        return str(self.processed_dir / processed_filename)

    def _get_job_file_paths(self, job_id: str) -> list[str]:
        """
        Get all file paths associated with a job.

        Args:
            job_id: Job identifier

        Returns:
            List of file paths for the job
        """
        file_paths = []

        # Find files in upload directory
        for file_path in self.upload_dir.glob(f"{job_id}_*"):
            file_paths.append(str(file_path))

        # Find files in processed directory
        for file_path in self.processed_dir.glob(f"{job_id}_*"):
            file_paths.append(str(file_path))

        return file_paths

    def cleanup_job_files(self, job_id: str) -> bool:
        """
        Clean up all files associated with a job.

        Args:
            job_id: Job identifier

        Returns:
            True if cleanup was successful
        """
        try:
            file_paths = self._get_job_file_paths(job_id)
            files_removed = 0

            for file_path in file_paths:
                try:
                    if os.path.exists(file_path):
                        os.unlink(file_path)
                        files_removed += 1
                except Exception as e:
                    logger.error(f"Error removing file {file_path}: {e}")

            if files_removed > 0:
                logger.info(f"Cleaned up {files_removed} files for job {job_id}")

            return True

        except Exception as e:
            logger.error(f"Error during cleanup for job {job_id}: {e}")
            return False

    def get_file_size(self, file_path: str) -> int:
        """Get file size in bytes."""
        try:
            return os.path.getsize(file_path)
        except Exception:
            return 0

    def file_exists(self, file_path: str) -> bool:
        """Check if file exists."""
        return os.path.exists(file_path) and os.path.isfile(file_path)
