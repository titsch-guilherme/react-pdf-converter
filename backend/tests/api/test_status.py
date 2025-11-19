"""Tests for status endpoints."""

from datetime import UTC, datetime
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

from app.schemas.status import JobStatus
from app.services.conversion import conversion_service


class TestStatusEndpoints:
    """Test cases for status endpoints."""

    def test_get_job_status_success(self, client: TestClient, auth_headers):
        """Test successful retrieval of job status."""
        mock_job_status = JobStatus(
            job_id="test-job-123",
            filename="test.pdf",
            status="processing",
            progress=50,
            created_at=datetime.now(UTC),
            updated_at=datetime.now(UTC),
            download_url=None,
            error=None,
        )

        with patch.object(
            conversion_service, "get_job_status", return_value=mock_job_status
        ):
            response = client.get("/api/v1/status/test-job-123", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert data["job_id"] == "test-job-123"
            assert data["filename"] == "test.pdf"
            assert data["status"] == "processing"
            assert data["progress"] == 50

    def test_get_job_status_not_found(self, client: TestClient, auth_headers):
        """Test job status when job doesn't exist."""
        with patch.object(conversion_service, "get_job_status", return_value=None):
            response = client.get(
                "/api/v1/status/nonexistent-job", headers=auth_headers
            )

            assert response.status_code == 404
            assert "Job not found" in response.json()["detail"]

    def test_get_job_status_without_auth(self, client: TestClient):
        """Test job status without authentication."""
        response = client.get("/api/v1/status/test-job-123")

        assert response.status_code == 401  # Unauthorized, not 422

    def test_get_job_status_service_error(self, client: TestClient, auth_headers):
        """Test job status when service throws an error."""
        with patch.object(
            conversion_service, "get_job_status", side_effect=Exception("Service error")
        ):
            response = client.get("/api/v1/status/test-job-123", headers=auth_headers)

            assert response.status_code == 500
            assert "Status service temporarily unavailable" in response.json()["detail"]

    def test_get_all_jobs_status_success(self, client: TestClient, auth_headers):
        """Test successful retrieval of all user jobs."""
        mock_jobs = [
            JobStatus(
                job_id="job-1",
                filename="file1.pdf",
                status="completed",
                progress=100,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url="/api/v1/download/job-1",
                error=None,
            ),
            JobStatus(
                job_id="job-2",
                filename="file2.pdf",
                status="processing",
                progress=75,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url=None,
                error=None,
            ),
            JobStatus(
                job_id="job-3",
                filename="file3.pdf",
                status="failed",
                progress=0,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url=None,
                error="Processing failed",
            ),
        ]

        with patch.object(conversion_service, "get_user_jobs", return_value=mock_jobs):
            response = client.get("/api/v1/status", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert "jobs" in data
            assert len(data["jobs"]) == 3

            # Check first job
            job1 = data["jobs"][0]
            assert job1["job_id"] == "job-1"
            assert job1["status"] == "completed"
            assert job1["progress"] == 100
            assert job1["download_url"] == "/api/v1/download/job-1"

            # Check second job
            job2 = data["jobs"][1]
            assert job2["job_id"] == "job-2"
            assert job2["status"] == "processing"
            assert job2["progress"] == 75

            # Check third job
            job3 = data["jobs"][2]
            assert job3["job_id"] == "job-3"
            assert job3["status"] == "failed"
            assert job3["error"] == "Processing failed"

    def test_get_all_jobs_status_empty(self, client: TestClient, auth_headers):
        """Test retrieval of all jobs when user has no jobs."""
        with patch.object(conversion_service, "get_user_jobs", return_value=[]):
            response = client.get("/api/v1/status", headers=auth_headers)

            assert response.status_code == 200
            data = response.json()
            assert "jobs" in data
            assert len(data["jobs"]) == 0

    def test_get_all_jobs_status_without_auth(self, client: TestClient):
        """Test all jobs status without authentication."""
        response = client.get("/api/v1/status")

        assert response.status_code == 401  # Unauthorized, not 422

    def test_get_all_jobs_status_service_error(self, client: TestClient, auth_headers):
        """Test all jobs status when service throws an error."""
        with patch.object(
            conversion_service, "get_user_jobs", side_effect=Exception("Service error")
        ):
            response = client.get("/api/v1/status", headers=auth_headers)

            assert response.status_code == 500
            assert "Status service temporarily unavailable" in response.json()["detail"]

    def test_batch_status_response_properties(self, client: TestClient, auth_headers):
        """Test BatchStatusResponse computed properties."""
        mock_jobs = [
            JobStatus(
                job_id="job-1",
                filename="file1.pdf",
                status="queued",
                progress=0,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url=None,
                error=None,
            ),
            JobStatus(
                job_id="job-2",
                filename="file2.pdf",
                status="processing",
                progress=50,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url=None,
                error=None,
            ),
            JobStatus(
                job_id="job-3",
                filename="file3.pdf",
                status="completed",
                progress=100,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url="/api/v1/download/job-3",
                error=None,
            ),
            JobStatus(
                job_id="job-4",
                filename="file4.pdf",
                status="failed",
                progress=0,
                created_at=datetime.now(UTC),
                updated_at=datetime.now(UTC),
                download_url=None,
                error="Processing failed",
            ),
        ]

        with patch.object(conversion_service, "get_user_jobs", return_value=mock_jobs):
            response = client.get("/api/v1/status", headers=auth_headers)

            assert response.status_code == 200

            # Test that we can access the response data
            data = response.json()
            jobs = data["jobs"]

            # Verify we have the expected job statuses
            statuses = [job["status"] for job in jobs]
            assert "queued" in statuses
            assert "processing" in statuses
            assert "completed" in statuses
            assert "failed" in statuses
