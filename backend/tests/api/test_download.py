"""Tests for download endpoints."""

import os
import tempfile
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.schemas.status import JobStatus
from app.services.conversion import conversion_service


class TestDownloadEndpoint:
    """Test cases for the download endpoint."""

    def test_download_completed_file_success(
        self, client: TestClient, auth_headers, sample_pdf_content
    ):
        """Test successful download of completed file."""
        # Create a temporary file to simulate processed output
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(sample_pdf_content)
            temp_file_path = temp_file.name

        try:
            # Mock the conversion service methods
            mock_job_status = JobStatus(
                job_id="test-job-123",
                filename="test.pdf",
                status="completed",
                progress=100,
                created_at="2025-01-01T00:00:00Z",
                updated_at="2025-01-01T00:05:00Z",
                download_url="/api/v1/download/test-job-123",
                error=None,
            )

            with (
                patch.object(
                    conversion_service, "get_job_status", return_value=mock_job_status
                ),
                patch.object(
                    conversion_service,
                    "get_download_file_path",
                    return_value=temp_file_path,
                ),
            ):
                response = client.get(
                    "/api/v1/download/test-job-123", headers=auth_headers
                )

                assert response.status_code == 200
                assert response.headers["content-type"] == "application/pdf"
                assert "attachment" in response.headers["content-disposition"]
                assert "test_searchable.pdf" in response.headers["content-disposition"]
                assert len(response.content) > 0

        finally:
            # Clean up temporary file
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)

    def test_download_job_not_found(self, client: TestClient, auth_headers):
        """Test download when job doesn't exist."""
        with patch.object(conversion_service, "get_job_status", return_value=None):
            response = client.get(
                "/api/v1/download/nonexistent-job", headers=auth_headers
            )

            assert response.status_code == 404
            assert "Job not found" in response.json()["detail"]

    def test_download_job_not_completed(self, client: TestClient, auth_headers):
        """Test download when job is not completed."""
        mock_job_status = JobStatus(
            job_id="test-job-123",
            filename="test.pdf",
            status="processing",
            progress=50,
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:02:00Z",
            download_url=None,
            error=None,
        )

        with patch.object(
            conversion_service, "get_job_status", return_value=mock_job_status
        ):
            response = client.get("/api/v1/download/test-job-123", headers=auth_headers)

            assert response.status_code == 400
            assert "Job is not completed" in response.json()["detail"]

    def test_download_file_not_found_on_disk(self, client: TestClient, auth_headers):
        """Test download when file doesn't exist on disk."""
        mock_job_status = JobStatus(
            job_id="test-job-123",
            filename="test.pdf",
            status="completed",
            progress=100,
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:05:00Z",
            download_url="/api/v1/download/test-job-123",
            error=None,
        )

        with (
            patch.object(
                conversion_service, "get_job_status", return_value=mock_job_status
            ),
            patch.object(
                conversion_service,
                "get_download_file_path",
                return_value="/nonexistent/path.pdf",
            ),
        ):
            response = client.get("/api/v1/download/test-job-123", headers=auth_headers)

            assert response.status_code == 404
            assert "Converted file not found on disk" in response.json()["detail"]

    def test_download_no_download_url(self, client: TestClient, auth_headers):
        """Test download when job has no download URL."""
        mock_job_status = JobStatus(
            job_id="test-job-123",
            filename="test.pdf",
            status="completed",
            progress=100,
            created_at="2025-01-01T00:00:00Z",
            updated_at="2025-01-01T00:05:00Z",
            download_url=None,
            error=None,
        )

        with patch.object(
            conversion_service, "get_job_status", return_value=mock_job_status
        ):
            response = client.get("/api/v1/download/test-job-123", headers=auth_headers)

            assert response.status_code == 404
            assert "Converted file not found" in response.json()["detail"]

    def test_download_without_auth(self, client: TestClient, sample_pdf_content):
        """Test download without authentication."""
        response = client.get("/api/v1/download/test-job-123")

        assert response.status_code == 401  # Unauthorized, not 422

    def test_download_service_error(self, client: TestClient, auth_headers):
        """Test download when service throws an error."""
        with patch.object(
            conversion_service, "get_job_status", side_effect=Exception("Service error")
        ):
            response = client.get("/api/v1/download/test-job-123", headers=auth_headers)

            assert response.status_code == 500
            assert (
                "Download service temporarily unavailable" in response.json()["detail"]
            )

    def test_download_filename_generation(
        self, client: TestClient, auth_headers, sample_pdf_content
    ):
        """Test proper filename generation for downloads."""
        with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as temp_file:
            temp_file.write(sample_pdf_content)
            temp_file_path = temp_file.name

        try:
            # Test with .pdf extension
            mock_job_status = JobStatus(
                job_id="test-job-123",
                filename="document.pdf",
                status="completed",
                progress=100,
                created_at="2025-01-01T00:00:00Z",
                updated_at="2025-01-01T00:05:00Z",
                download_url="/api/v1/download/test-job-123",
                error=None,
            )

            with (
                patch.object(
                    conversion_service, "get_job_status", return_value=mock_job_status
                ),
                patch.object(
                    conversion_service,
                    "get_download_file_path",
                    return_value=temp_file_path,
                ),
            ):
                response = client.get(
                    "/api/v1/download/test-job-123", headers=auth_headers
                )

                assert response.status_code == 200
                assert (
                    "document_searchable.pdf" in response.headers["content-disposition"]
                )

            # Test without .pdf extension
            mock_job_status.filename = "document"
            with (
                patch.object(
                    conversion_service, "get_job_status", return_value=mock_job_status
                ),
                patch.object(
                    conversion_service,
                    "get_download_file_path",
                    return_value=temp_file_path,
                ),
            ):
                response = client.get(
                    "/api/v1/download/test-job-123", headers=auth_headers
                )

                assert response.status_code == 200
                assert (
                    "document_searchable.pdf" in response.headers["content-disposition"]
                )

        finally:
            if os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
