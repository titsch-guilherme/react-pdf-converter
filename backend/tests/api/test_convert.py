"""Test PDF conversion endpoints."""

import io

from fastapi.testclient import TestClient


class TestConvertEndpoint:
    """Test PDF conversion functionality."""

    def test_convert_single_pdf(
        self, client: TestClient, auth_headers, sample_pdf_content
    ):
        """Test converting a single PDF file."""
        files = {
            "files": ("test.pdf", io.BytesIO(sample_pdf_content), "application/pdf")
        }

        response = client.post("/api/v1/convert", files=files, headers=auth_headers)

        assert response.status_code == 200

        data = response.json()
        assert "jobs" in data
        assert len(data["jobs"]) == 1

        job = data["jobs"][0]
        assert "job_id" in job
        assert job["filename"] == "test.pdf"
        assert job["status"] in ["queued", "processing"]

    def test_convert_multiple_pdfs(
        self, client: TestClient, auth_headers, sample_pdf_content
    ):
        """Test converting multiple PDF files."""
        files = [
            ("files", ("test1.pdf", io.BytesIO(sample_pdf_content), "application/pdf")),
            ("files", ("test2.pdf", io.BytesIO(sample_pdf_content), "application/pdf")),
        ]

        response = client.post("/api/v1/convert", files=files, headers=auth_headers)

        assert response.status_code == 200

        data = response.json()
        assert len(data["jobs"]) == 2

        filenames = [job["filename"] for job in data["jobs"]]
        assert "test1.pdf" in filenames
        assert "test2.pdf" in filenames

    def test_convert_without_auth(self, client: TestClient, sample_pdf_content):
        """Test conversion without authentication."""
        files = {
            "files": ("test.pdf", io.BytesIO(sample_pdf_content), "application/pdf")
        }

        response = client.post("/api/v1/convert", files=files)

        assert response.status_code == 401

    def test_convert_invalid_file_type(self, client: TestClient, auth_headers):
        """Test conversion with invalid file type."""
        files = {"files": ("test.txt", io.BytesIO(b"Not a PDF"), "text/plain")}

        response = client.post("/api/v1/convert", files=files, headers=auth_headers)

        assert response.status_code == 400

        data = response.json()
        assert "validation failed" in data["detail"].lower()

    def test_convert_empty_file(self, client: TestClient, auth_headers):
        """Test conversion with empty file."""
        files = {"files": ("empty.pdf", io.BytesIO(b""), "application/pdf")}

        response = client.post("/api/v1/convert", files=files, headers=auth_headers)

        assert response.status_code == 400

        data = response.json()
        assert "empty" in data["detail"].lower()

    def test_convert_too_many_files(
        self, client: TestClient, auth_headers, sample_pdf_content
    ):
        """Test conversion with too many files."""
        # Create more files than the limit (assuming limit is 10)
        files = []
        for i in range(15):  # Exceed the limit
            files.append(
                (
                    "files",
                    (f"test{i}.pdf", io.BytesIO(sample_pdf_content), "application/pdf"),
                )
            )

        response = client.post("/api/v1/convert", files=files, headers=auth_headers)

        assert response.status_code == 400

        data = response.json()
        assert "too many files" in data["detail"].lower()

    def test_convert_no_files(self, client: TestClient, auth_headers):
        """Test conversion with no files provided."""
        response = client.post("/api/v1/convert", headers=auth_headers)

        assert response.status_code == 422  # FastAPI validation error
