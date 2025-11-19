"""Test conversion service."""

from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock

import pytest
from fastapi import UploadFile

from app.services.conversion import ConversionJob, ConversionService


class TestConversionJob:
    """Test ConversionJob class."""

    def test_job_creation(self):
        """Test creating a conversion job."""
        job = ConversionJob(
            job_id="test-job-123",
            filename="test.pdf",
            user_id="user-123",
            session_id="session-123",
            file_path="/tmp/test.pdf",
        )

        assert job.job_id == "test-job-123"
        assert job.filename == "test.pdf"
        assert job.user_id == "user-123"
        assert job.status == "queued"
        assert job.progress == 0
        assert job.error is None

    def test_job_status_update(self):
        """Test updating job status."""
        job = ConversionJob(
            job_id="test-job-123",
            filename="test.pdf",
            user_id="user-123",
            session_id="session-123",
            file_path="/tmp/test.pdf",
        )

        job.update_status("processing", progress=50)

        assert job.status == "processing"
        assert job.progress == 50
        assert job.error is None

    def test_job_error_update(self):
        """Test updating job with error."""
        job = ConversionJob(
            job_id="test-job-123",
            filename="test.pdf",
            user_id="user-123",
            session_id="session-123",
            file_path="/tmp/test.pdf",
        )

        job.update_status("failed", error="OCR processing failed")

        assert job.status == "failed"
        assert job.error == "OCR processing failed"

    def test_job_to_status(self):
        """Test converting job to status schema."""
        job = ConversionJob(
            job_id="test-job-123",
            filename="test.pdf",
            user_id="user-123",
            session_id="session-123",
            file_path="/tmp/test.pdf",
        )

        status = job.to_status()

        assert status.job_id == "test-job-123"
        assert status.filename == "test.pdf"
        assert status.status == "queued"
        assert status.progress == 0


class TestConversionService:
    """Test ConversionService class."""

    @pytest.fixture
    def service(self):
        """Create a conversion service instance."""
        return ConversionService()

    @pytest.fixture
    def mock_upload_file(self, sample_pdf_content):
        """Create a mock UploadFile."""
        mock_file = MagicMock(spec=UploadFile)
        mock_file.filename = "test.pdf"
        mock_file.read = AsyncMock(return_value=sample_pdf_content)
        return mock_file

    async def test_start_conversion(self, service, mock_upload_file):
        """Test starting a conversion job."""
        job_id = await service.start_conversion(
            file=mock_upload_file, user_id="user-123", session_id="session-123"
        )

        assert job_id is not None
        assert job_id in service.jobs

        job = service.jobs[job_id]
        assert job.filename == "test.pdf"
        assert job.user_id == "user-123"
        assert job.status == "queued"

    async def test_get_job_status(self, service, mock_upload_file):
        """Test getting job status."""
        job_id = await service.start_conversion(
            file=mock_upload_file, user_id="user-123", session_id="session-123"
        )

        status = await service.get_job_status(job_id, "user-123")

        assert status is not None
        assert status.job_id == job_id
        assert status.filename == "test.pdf"

    async def test_get_job_status_wrong_user(self, service, mock_upload_file):
        """Test getting job status with wrong user."""
        job_id = await service.start_conversion(
            file=mock_upload_file, user_id="user-123", session_id="session-123"
        )

        status = await service.get_job_status(job_id, "different-user")

        assert status is None

    async def test_get_user_jobs(self, service, mock_upload_file):
        """Test getting all jobs for a user."""
        # Start multiple jobs
        job_id1 = await service.start_conversion(
            file=mock_upload_file, user_id="user-123", session_id="session-123"
        )

        mock_upload_file.filename = "test2.pdf"
        job_id2 = await service.start_conversion(
            file=mock_upload_file, user_id="user-123", session_id="session-123"
        )

        jobs = await service.get_user_jobs("user-123")

        assert len(jobs) == 2
        job_ids = [job.job_id for job in jobs]
        assert job_id1 in job_ids
        assert job_id2 in job_ids

    async def test_get_user_jobs_empty(self, service):
        """Test getting jobs for user with no jobs."""
        jobs = await service.get_user_jobs("user-with-no-jobs")

        assert len(jobs) == 0

    def test_cleanup_old_jobs(self, service):
        """Test cleaning up old jobs."""
        # Create a job and manually set old timestamp
        job = ConversionJob(
            job_id="old-job",
            filename="old.pdf",
            user_id="user-123",
            session_id="session-123",
            file_path="/tmp/old.pdf",
        )

        # Make it old using timezone-aware datetime
        job.created_at = datetime.now(UTC) - timedelta(hours=25)

        service.jobs["old-job"] = job
        service.user_jobs["user-123"] = ["old-job"]

        # Cleanup jobs older than 24 hours
        cleaned_count = service.cleanup_old_jobs(max_age_hours=24)

        assert cleaned_count == 1
        assert "old-job" not in service.jobs
        assert "old-job" not in service.user_jobs.get("user-123", [])
