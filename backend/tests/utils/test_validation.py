"""Test validation utilities."""

import io
from unittest.mock import MagicMock

from fastapi import UploadFile

from app.utils.validation import (
    sanitize_filename,
    validate_pdf_content,
    validate_pdf_files,
)


class TestPDFValidation:
    """Test PDF file validation."""

    def create_mock_file(
        self, filename: str, content: bytes, content_type: str = "application/pdf"
    ):
        """Create a mock UploadFile."""
        mock_file = MagicMock(spec=UploadFile)
        mock_file.filename = filename
        mock_file.file = io.BytesIO(content)
        mock_file.content_type = content_type

        # Mock the read method
        async def mock_read(size=-1):
            return content

        mock_file.read = mock_read
        return mock_file

    async def test_validate_single_valid_pdf(self, sample_pdf_content):
        """Test validating a single valid PDF."""
        files = [self.create_mock_file("test.pdf", sample_pdf_content)]

        result = await validate_pdf_files(files)

        assert result.is_valid
        assert result.error_message == ""

    async def test_validate_multiple_valid_pdfs(self, sample_pdf_content):
        """Test validating multiple valid PDFs."""
        files = [
            self.create_mock_file("test1.pdf", sample_pdf_content),
            self.create_mock_file("test2.pdf", sample_pdf_content),
        ]

        result = await validate_pdf_files(files)

        assert result.is_valid

    async def test_validate_no_files(self):
        """Test validation with no files."""
        result = await validate_pdf_files([])

        assert not result.is_valid
        assert "No files provided" in result.error_message

    async def test_validate_too_many_files(self, sample_pdf_content):
        """Test validation with too many files."""
        # Create 15 files (assuming limit is 10)
        files = []
        for i in range(15):
            files.append(self.create_mock_file(f"test{i}.pdf", sample_pdf_content))

        result = await validate_pdf_files(files)

        assert not result.is_valid
        assert "Too many files" in result.error_message

    async def test_validate_invalid_extension(self, sample_pdf_content):
        """Test validation with invalid file extension."""
        files = [self.create_mock_file("test.txt", sample_pdf_content)]

        result = await validate_pdf_files(files)

        assert not result.is_valid
        assert "Only PDF files are allowed" in result.error_message

    async def test_validate_empty_file(self):
        """Test validation with empty file."""
        files = [self.create_mock_file("test.pdf", b"")]

        result = await validate_pdf_files(files)

        assert not result.is_valid
        assert "File is empty" in result.error_message

    async def test_validate_missing_filename(self, sample_pdf_content):
        """Test validation with missing filename."""
        files = [self.create_mock_file("", sample_pdf_content)]

        result = await validate_pdf_files(files)

        assert not result.is_valid
        assert "Missing filename" in result.error_message

    async def test_validate_invalid_pdf_content(self):
        """Test validation with invalid PDF content."""
        files = [self.create_mock_file("test.pdf", b"Not a PDF file")]

        result = await validate_pdf_files(files)

        assert not result.is_valid
        assert "Invalid PDF content" in result.error_message


class TestPDFContentValidation:
    """Test PDF content validation."""

    def create_mock_file(self, content: bytes):
        """Create a mock UploadFile with content."""
        mock_file = MagicMock(spec=UploadFile)
        mock_file.file = io.BytesIO(content)

        async def mock_read(size=-1):
            return content

        mock_file.read = mock_read
        return mock_file

    async def test_valid_pdf_content(self, sample_pdf_content):
        """Test valid PDF content validation."""
        mock_file = self.create_mock_file(sample_pdf_content)

        result = await validate_pdf_content(mock_file)

        assert result is True

    async def test_invalid_pdf_content(self):
        """Test invalid PDF content validation."""
        mock_file = self.create_mock_file(b"Not a PDF")

        result = await validate_pdf_content(mock_file)

        assert result is False

    async def test_empty_pdf_content(self):
        """Test empty PDF content validation."""
        mock_file = self.create_mock_file(b"")

        result = await validate_pdf_content(mock_file)

        assert result is False


class TestFilenameSanitization:
    """Test filename sanitization."""

    def test_sanitize_normal_filename(self):
        """Test sanitizing a normal filename."""
        result = sanitize_filename("document.pdf")
        assert result == "document.pdf"

    def test_sanitize_dangerous_characters(self):
        """Test sanitizing filename with dangerous characters."""
        result = sanitize_filename("doc<>ument.pdf")
        assert result == "doc__ument.pdf"

    def test_sanitize_path_traversal(self):
        """Test sanitizing filename with path traversal."""
        result = sanitize_filename("../../../etc/passwd")
        assert result == "passwd"

    def test_sanitize_empty_filename(self):
        """Test sanitizing empty filename."""
        result = sanitize_filename("")
        assert result == "unnamed_file.pdf"

    def test_sanitize_long_filename(self):
        """Test sanitizing very long filename."""
        long_name = "a" * 300 + ".pdf"
        result = sanitize_filename(long_name)
        assert len(result) <= 255
        assert result.endswith(".pdf")

    def test_sanitize_dots_and_spaces(self):
        """Test sanitizing filename with leading/trailing dots and spaces."""
        result = sanitize_filename("  ..document.pdf..  ")
        assert result == "document.pdf"
