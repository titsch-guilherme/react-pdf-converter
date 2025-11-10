"""Test authentication endpoints."""

from unittest.mock import patch

from fastapi.testclient import TestClient


class TestAuthValidation:
    """Test authentication token validation."""

    @patch("app.core.security.oauth_validator.validate_token")
    def test_validate_token_success(self, mock_validate, client: TestClient):
        """Test successful token validation."""
        # Mock successful validation
        mock_validate.return_value = {
            "user_id": "123456789",
            "email": "test@example.com",
            "name": "Test User",
            "picture": "https://example.com/photo.jpg",
            "scopes": ["https://www.googleapis.com/auth/drive.file"],
        }

        response = client.post(
            "/api/v1/auth/validate", json={"access_token": "valid_token"}
        )

        assert response.status_code == 200

        data = response.json()
        assert "session_id" in data
        assert data["user_id"] == "123456789"
        assert "expires_at" in data
        assert data["user_info"]["email"] == "test@example.com"

    @patch("app.core.security.oauth_validator.validate_token")
    def test_validate_token_invalid(self, mock_validate, client: TestClient):
        """Test invalid token validation."""
        # Mock failed validation
        mock_validate.return_value = None

        response = client.post(
            "/api/v1/auth/validate", json={"access_token": "invalid_token"}
        )

        assert response.status_code == 401

        data = response.json()
        assert "detail" in data
        assert "Invalid or expired" in data["detail"]

    def test_validate_token_missing_token(self, client: TestClient):
        """Test validation with missing token."""
        response = client.post("/api/v1/auth/validate", json={})

        assert response.status_code == 422  # Validation error

    def test_validate_token_empty_token(self, client: TestClient):
        """Test validation with empty token."""
        response = client.post("/api/v1/auth/validate", json={"access_token": ""})

        assert response.status_code == 401


class TestAuthLogout:
    """Test logout functionality."""

    def test_logout_success(self, client: TestClient, mock_session):
        """Test successful logout."""
        session_id = mock_session["session_id"]

        response = client.post("/api/v1/auth/logout", params={"session_id": session_id})

        assert response.status_code == 200

        data = response.json()
        assert data["message"] == "Successfully logged out"

    def test_logout_invalid_session(self, client: TestClient):
        """Test logout with invalid session."""
        response = client.post(
            "/api/v1/auth/logout", params={"session_id": "invalid_session"}
        )

        assert response.status_code == 404

        data = response.json()
        assert "Session not found" in data["detail"]
