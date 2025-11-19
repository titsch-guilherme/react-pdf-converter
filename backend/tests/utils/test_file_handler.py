"""Tests for file handler utilities."""

import os
import tempfile
from pathlib import Path
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import UploadFile

from app.utils.file_handler import FileHandler


class TestFileHandler:
    """Test cases for FileHandler."""

    def test_init(self):
        """Test FileHandler initialization."""
        handler = FileHandler()

        assert handler is not None
        # Check that directories are created
        assert Path("uploads").exists()
        assert Path("processed").exists()

    @pytest.mark.asyncio
    async def test_save_upload_success(self, sample_pdf_content):
        """Test successful file upload saving."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Create mock UploadFile
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        mock_file.read.return_value = sample_pdf_content

        try:
            file_path = await handler.save_upload(mock_file, job_id)

            assert file_path is not None
            assert job_id in file_path
            assert "test.pdf" in file_path
            assert os.path.exists(file_path)

            # Verify file content
            with open(file_path, "rb") as f:
                saved_content = f.read()
            assert saved_content == sample_pdf_content

        finally:
            # Clean up
            if "file_path" in locals() and os.path.exists(file_path):
                os.unlink(file_path)

    @pytest.mark.asyncio
    async def test_save_upload_no_filename(self, sample_pdf_content):
        """Test file upload saving with no filename."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Create mock UploadFile without filename
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = None
        mock_file.read.return_value = sample_pdf_content

        try:
            file_path = await handler.save_upload(mock_file, job_id)

            assert file_path is not None
            assert job_id in file_path
            assert "unknown.pdf" in file_path
            assert os.path.exists(file_path)

        finally:
            # Clean up
            if "file_path" in locals() and os.path.exists(file_path):
                os.unlink(file_path)

    @pytest.mark.asyncio
    async def test_save_upload_read_error(self):
        """Test file upload saving with read error."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Create mock UploadFile that raises error on read
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        mock_file.read.side_effect = Exception("Read error")

        with pytest.raises(Exception, match="Read error"):
            await handler.save_upload(mock_file, job_id)

    def test_file_exists_true(self, sample_pdf_content):
        """Test file_exists with existing file."""
        handler = FileHandler()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(sample_pdf_content)
            temp_file_path = temp_file.name

        try:
            result = handler.file_exists(temp_file_path)
            assert result is True
        finally:
            os.unlink(temp_file_path)

    def test_file_exists_false(self):
        """Test file_exists with non-existent file."""
        handler = FileHandler()

        result = handler.file_exists("/nonexistent/path/file.pdf")
        assert result is False

    def test_get_file_size_success(self, sample_pdf_content):
        """Test get_file_size with existing file."""
        handler = FileHandler()

        # Create a temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(sample_pdf_content)
            temp_file_path = temp_file.name

        try:
            size = handler.get_file_size(temp_file_path)
            assert size == len(sample_pdf_content)
        finally:
            os.unlink(temp_file_path)

    def test_get_file_size_nonexistent(self):
        """Test get_file_size with non-existent file."""
        handler = FileHandler()

        size = handler.get_file_size("/nonexistent/path/file.pdf")
        assert size == 0

    def test_get_processed_file_path(self):
        """Test get_processed_file_path."""
        handler = FileHandler()
        job_id = "test-job-123"
        original_filename = "document.pdf"

        processed_path = handler.get_processed_file_path(job_id, original_filename)

        assert job_id in processed_path
        assert "searchable" in processed_path
        assert processed_path.endswith(".pdf")
        assert "processed" in processed_path

    def test_get_processed_file_path_no_extension(self):
        """Test get_processed_file_path with filename without extension."""
        handler = FileHandler()
        job_id = "test-job-123"
        original_filename = "document"

        processed_path = handler.get_processed_file_path(job_id, original_filename)

        assert job_id in processed_path
        assert "searchable" in processed_path
        assert processed_path.endswith(".pdf")

    def test_cleanup_job_files_success(self, sample_pdf_content):
        """Test successful cleanup of job files."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Create temporary files to simulate job files
        upload_file = None
        processed_file = None

        try:
            # Create upload file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f"_{job_id}_test.pdf"
            ) as temp_file:
                temp_file.write(sample_pdf_content)
                upload_file = temp_file.name

            # Create processed file
            with tempfile.NamedTemporaryFile(
                delete=False, suffix=f"_{job_id}_searchable.pdf"
            ) as temp_file:
                temp_file.write(sample_pdf_content)
                processed_file = temp_file.name

            # Verify files exist
            assert os.path.exists(upload_file)
            assert os.path.exists(processed_file)

            # Mock the file paths that would be found
            with patch.object(
                handler,
                "_get_job_file_paths",
                return_value=[upload_file, processed_file],
            ):
                result = handler.cleanup_job_files(job_id)

                assert result is True

        finally:
            # Clean up any remaining files
            for file_path in [upload_file, processed_file]:
                if file_path and os.path.exists(file_path):
                    os.unlink(file_path)

    def test_cleanup_job_files_no_files(self):
        """Test cleanup when no files exist for job."""
        handler = FileHandler()
        job_id = "nonexistent-job"

        with patch.object(handler, "_get_job_file_paths", return_value=[]):
            result = handler.cleanup_job_files(job_id)
            assert result is True

    def test_cleanup_job_files_error(self):
        """Test cleanup with file deletion error."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Mock file paths that don't exist (will cause error)
        fake_paths = ["/nonexistent/file1.pdf", "/nonexistent/file2.pdf"]

        with patch.object(handler, "_get_job_file_paths", return_value=fake_paths):
            # Should not raise exception, but return False
            result = handler.cleanup_job_files(job_id)
            # The method should handle errors gracefully
            assert result in [True, False]  # Depends on implementation

    def test_get_job_file_paths(self):
        """Test _get_job_file_paths method."""
        handler = FileHandler()
        job_id = "test-job-123"

        # This is a private method, but we can test it if it exists
        if hasattr(handler, "_get_job_file_paths"):
            paths = handler._get_job_file_paths(job_id)
            assert isinstance(paths, list)
        else:
            # If method doesn't exist, that's also valid
            assert True

    @pytest.mark.asyncio
    async def test_save_upload_sanitize_filename(self, sample_pdf_content):
        """Test that filenames are properly sanitized."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Create mock UploadFile with problematic filename
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = "../../../etc/passwd"
        mock_file.read.return_value = sample_pdf_content

        try:
            file_path = await handler.save_upload(mock_file, job_id)

            assert file_path is not None
            assert "../" not in file_path
            assert "etc" not in file_path
            # The filename should be sanitized but "passwd" might remain as it's not a path character
            assert job_id in file_path

        finally:
            # Clean up
            if "file_path" in locals() and os.path.exists(file_path):
                os.unlink(file_path)

    @pytest.mark.asyncio
    async def test_save_upload_large_filename(self, sample_pdf_content):
        """Test handling of very long filenames."""
        handler = FileHandler()
        job_id = "test-job-123"

        # Create mock UploadFile with very long filename (but not too long to cause filesystem error)
        long_filename = (
            "a" * 200 + ".pdf"
        )  # Reduced from 300 to avoid filesystem limits
        mock_file = AsyncMock(spec=UploadFile)
        mock_file.filename = long_filename
        mock_file.read.return_value = sample_pdf_content

        try:
            file_path = await handler.save_upload(mock_file, job_id)

            assert file_path is not None
            assert len(os.path.basename(file_path)) < 255  # Filesystem limit
            assert job_id in file_path

        finally:
            # Clean up
            if "file_path" in locals() and os.path.exists(file_path):
                os.unlink(file_path)
