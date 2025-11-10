"""Test health check endpoint."""

from fastapi.testclient import TestClient


def test_health_check(client: TestClient):
    """Test the health check endpoint."""
    response = client.get("/health")

    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data

    # Check response headers
    assert "X-Request-ID" in response.headers
    assert "X-Process-Time" in response.headers


def test_health_check_response_structure(client: TestClient):
    """Test that health check returns expected structure."""
    response = client.get("/health")

    data = response.json()

    # Required fields
    required_fields = ["status", "version", "environment"]
    for field in required_fields:
        assert field in data, f"Missing required field: {field}"

    # Check data types
    assert isinstance(data["status"], str)
    assert isinstance(data["version"], str)
    assert isinstance(data["environment"], str)
