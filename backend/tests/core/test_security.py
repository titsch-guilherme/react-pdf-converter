"""Tests for security module."""

import asyncio
from datetime import UTC, datetime, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

import httpx
import pytest

from app.core.security import (
    GoogleOAuthValidator,
    SessionManager,
    generate_request_id,
    hash_file_content,
)


class TestSessionManager:
    """Test cases for SessionManager."""

    def test_create_session(self):
        """Test session creation."""
        manager = SessionManager()
        user_id = "test-user-123"
        user_info = {"email": "test@example.com", "name": "Test User"}

        session_id = manager.create_session(user_id, user_info)

        assert session_id is not None
        assert len(session_id) > 0
        assert session_id in manager._sessions

        session = manager._sessions[session_id]
        assert session["user_id"] == user_id
        assert session["user_info"] == user_info
        assert "created_at" in session
        assert "expires_at" in session
        assert "last_accessed" in session

    def test_get_session_valid(self):
        """Test getting a valid session."""
        manager = SessionManager()
        user_id = "test-user-123"
        user_info = {"email": "test@example.com"}

        session_id = manager.create_session(user_id, user_info)
        retrieved_session = manager.get_session(session_id)

        assert retrieved_session is not None
        assert retrieved_session["user_id"] == user_id
        assert retrieved_session["user_info"] == user_info

    def test_get_session_nonexistent(self):
        """Test getting a non-existent session."""
        manager = SessionManager()

        retrieved_session = manager.get_session("nonexistent-session")

        assert retrieved_session is None

    def test_get_session_expired(self):
        """Test getting an expired session."""
        manager = SessionManager()
        user_id = "test-user-123"
        user_info = {"email": "test@example.com"}

        session_id = manager.create_session(user_id, user_info)

        # Manually expire the session
        session = manager._sessions[session_id]
        session["expires_at"] = datetime.now(UTC) - timedelta(hours=1)

        retrieved_session = manager.get_session(session_id)

        assert retrieved_session is None
        assert session_id not in manager._sessions  # Should be deleted

    def test_delete_session_existing(self):
        """Test deleting an existing session."""
        manager = SessionManager()
        user_id = "test-user-123"
        user_info = {"email": "test@example.com"}

        session_id = manager.create_session(user_id, user_info)
        result = manager.delete_session(session_id)

        assert result is True
        assert session_id not in manager._sessions

    def test_delete_session_nonexistent(self):
        """Test deleting a non-existent session."""
        manager = SessionManager()

        result = manager.delete_session("nonexistent-session")

        assert result is False

    def test_cleanup_expired_sessions(self):
        """Test cleanup of expired sessions."""
        manager = SessionManager()

        # Create some sessions
        session1 = manager.create_session("user1", {"email": "user1@example.com"})
        session2 = manager.create_session("user2", {"email": "user2@example.com"})
        session3 = manager.create_session("user3", {"email": "user3@example.com"})

        # Expire some sessions
        manager._sessions[session1]["expires_at"] = datetime.now(UTC) - timedelta(
            hours=1
        )
        manager._sessions[session2]["expires_at"] = datetime.now(UTC) - timedelta(
            hours=2
        )
        # session3 remains valid

        cleaned_count = manager.cleanup_expired_sessions()

        assert cleaned_count == 2
        assert session1 not in manager._sessions
        assert session2 not in manager._sessions
        assert session3 in manager._sessions

    def test_session_last_accessed_update(self):
        """Test that last_accessed is updated when getting session."""
        manager = SessionManager()
        user_id = "test-user-123"
        user_info = {"email": "test@example.com"}

        session_id = manager.create_session(user_id, user_info)
        original_last_accessed = manager._sessions[session_id]["last_accessed"]

        # Small delay to ensure timestamp difference
        import time

        time.sleep(0.01)

        manager.get_session(session_id)
        updated_last_accessed = manager._sessions[session_id]["last_accessed"]

        assert updated_last_accessed > original_last_accessed

    def test_generate_session_id_uniqueness(self):
        """Test that session IDs are unique."""
        manager = SessionManager()

        session_ids = set()
        for _ in range(100):
            session_id = manager._generate_session_id()
            assert session_id not in session_ids
            session_ids.add(session_id)


class TestGoogleOAuthValidator:
    """Test cases for GoogleOAuthValidator."""

    @pytest.mark.asyncio
    async def test_validate_token_success(self):
        """Test successful token validation."""
        validator = GoogleOAuthValidator()

        mock_response_data = {
            "sub": "123456789",
            "email": "test@example.com",
            "email_verified": True,
            "name": "Test User",
            "picture": "https://example.com/photo.jpg",
            "scope": "openid email profile",
        }

        # Create a proper mock response
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data

        # Mock the async client context manager
        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("valid-token")

            assert result is not None
            assert result["user_id"] == "123456789"
            assert result["email"] == "test@example.com"
            assert result["name"] == "Test User"
            assert result["picture"] == "https://example.com/photo.jpg"
            assert result["scopes"] == ["openid", "email", "profile"]

    @pytest.mark.asyncio
    async def test_validate_token_invalid_response(self):
        """Test token validation with invalid response."""
        validator = GoogleOAuthValidator()

        mock_response = MagicMock()
        mock_response.status_code = 400

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("invalid-token")

            assert result is None

    @pytest.mark.asyncio
    async def test_validate_token_missing_fields(self):
        """Test token validation with missing required fields."""
        validator = GoogleOAuthValidator()

        mock_response_data = {
            "sub": "123456789",
            # Missing email and email_verified
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("token-missing-fields")

            assert result is None

    @pytest.mark.asyncio
    async def test_validate_token_unverified_email(self):
        """Test token validation with unverified email."""
        validator = GoogleOAuthValidator()

        mock_response_data = {
            "sub": "123456789",
            "email": "test@example.com",
            "email_verified": False,  # Email not verified
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("unverified-email-token")

            assert result is None

    @pytest.mark.asyncio
    async def test_validate_token_timeout(self):
        """Test token validation with timeout."""
        validator = GoogleOAuthValidator()

        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.TimeoutException("Timeout")

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("timeout-token")

            assert result is None

    @pytest.mark.asyncio
    async def test_validate_token_request_error(self):
        """Test token validation with request error."""
        validator = GoogleOAuthValidator()

        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = httpx.RequestError("Network error")

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("error-token")

            assert result is None

    @pytest.mark.asyncio
    async def test_validate_token_unexpected_error(self):
        """Test token validation with unexpected error."""
        validator = GoogleOAuthValidator()

        mock_client_instance = AsyncMock()
        mock_client_instance.get.side_effect = Exception("Unexpected error")

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("unexpected-error-token")

            assert result is None

    @pytest.mark.asyncio
    async def test_validate_token_no_scope(self):
        """Test token validation with no scope field."""
        validator = GoogleOAuthValidator()

        mock_response_data = {
            "sub": "123456789",
            "email": "test@example.com",
            "email_verified": True,
            "name": "Test User",
            # No scope field
        }

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = mock_response_data

        mock_client_instance = AsyncMock()
        mock_client_instance.get.return_value = mock_response

        with patch("httpx.AsyncClient") as mock_client_class:
            mock_client_class.return_value.__aenter__.return_value = (
                mock_client_instance
            )

            result = await validator.validate_token("no-scope-token")

            assert result is not None
            assert result["scopes"] == []


class TestUtilityFunctions:
    """Test cases for utility functions."""

    def test_generate_request_id(self):
        """Test request ID generation."""
        request_id = generate_request_id()

        assert request_id is not None
        assert len(request_id) > 0
        assert isinstance(request_id, str)

        # Test uniqueness
        request_ids = set()
        for _ in range(100):
            rid = generate_request_id()
            assert rid not in request_ids
            request_ids.add(rid)

    def test_hash_file_content(self):
        """Test file content hashing."""
        content1 = b"This is test content"
        content2 = b"This is different content"
        content3 = b"This is test content"  # Same as content1

        hash1 = hash_file_content(content1)
        hash2 = hash_file_content(content2)
        hash3 = hash_file_content(content3)

        assert hash1 != hash2  # Different content should have different hashes
        assert hash1 == hash3  # Same content should have same hash
        assert len(hash1) == 64  # SHA-256 produces 64-character hex string
        assert all(c in "0123456789abcdef" for c in hash1)  # Should be valid hex

    def test_hash_file_content_empty(self):
        """Test hashing empty content."""
        empty_content = b""
        hash_result = hash_file_content(empty_content)

        assert hash_result is not None
        assert len(hash_result) == 64
        # SHA-256 of empty string is a known value
        assert (
            hash_result
            == "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
        )
