"""File validation utilities."""

from typing import NamedTuple

import magic
from fastapi import UploadFile
from loguru import logger

from app.core.config import settings


class ValidationResult(NamedTuple):
    """Result of file validation."""

    is_valid: bool
    error_message: str = ""


async def validate_pdf_files(files: list[UploadFile]) -> ValidationResult:
    """
    Validate uploaded PDF files.

    Checks:
    - File count within limits
    - File size within limits
    - File type is PDF
    - File content is valid PDF
    """
    try:
        # Check file count
        if len(files) > settings.MAX_FILES_PER_BATCH:
            return ValidationResult(
                is_valid=False,
                error_message=f"Too many files. Maximum {settings.MAX_FILES_PER_BATCH} files allowed per batch.",
            )

        if len(files) == 0:
            return ValidationResult(is_valid=False, error_message="No files provided.")

        # Validate each file
        for i, file in enumerate(files):
            # Check filename
            if not file.filename:
                return ValidationResult(
                    is_valid=False, error_message=f"File {i + 1}: Missing filename."
                )

            # Check file extension
            if not file.filename.lower().endswith(".pdf"):
                return ValidationResult(
                    is_valid=False,
                    error_message=f"File '{file.filename}': Only PDF files are allowed.",
                )

            # Check file size
            file.file.seek(0, 2)  # Seek to end
            file_size = file.file.tell()
            file.file.seek(0)  # Reset to beginning

            if file_size > settings.max_file_size_bytes:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"File '{file.filename}': Size {file_size / (1024 * 1024):.1f}MB exceeds maximum {settings.MAX_FILE_SIZE_MB}MB.",
                )

            if file_size == 0:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"File '{file.filename}': File is empty.",
                )

            # Check file content type
            content_valid = await validate_pdf_content(file)
            if not content_valid:
                return ValidationResult(
                    is_valid=False,
                    error_message=f"File '{file.filename}': Invalid PDF content or corrupted file.",
                )

        logger.info(f"Successfully validated {len(files)} PDF files")
        return ValidationResult(is_valid=True)

    except Exception as e:
        logger.error(f"Error during file validation: {e}")
        return ValidationResult(
            is_valid=False, error_message="File validation failed due to server error."
        )


async def validate_pdf_content(file: UploadFile) -> bool:
    """
    Validate that the file content is actually a PDF.

    Uses python-magic to check the file's MIME type based on content,
    not just the filename extension.
    """
    try:
        # Read first chunk of file for magic number detection
        chunk = await file.read(2048)
        file.file.seek(0)  # Reset file position

        # Check PDF magic number (starts with %PDF)
        if chunk.startswith(b"%PDF"):
            return True

        # Fallback: use python-magic if available
        try:
            mime_type = magic.from_buffer(chunk, mime=True)
            return mime_type == "application/pdf"
        except Exception:
            # If magic is not available, just check the PDF header
            return chunk.startswith(b"%PDF")

    except Exception as e:
        logger.error(f"Error validating PDF content: {e}")
        return False


def sanitize_filename(filename: str) -> str:
    """
    Sanitize filename to prevent path traversal and other security issues.
    """
    import os
    import re

    # Get just the filename without path
    filename = os.path.basename(filename)

    # Remove or replace dangerous characters
    filename = re.sub(r'[<>:"/\\|?*]', "_", filename)

    # Remove leading/trailing dots and spaces
    filename = filename.strip(". ")

    # Ensure filename is not empty
    if not filename:
        filename = "unnamed_file.pdf"

    # Limit length
    if len(filename) > 255:
        name, ext = os.path.splitext(filename)
        filename = name[:251] + ext

    return filename
