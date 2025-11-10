"""Pytest configuration and fixtures."""

import asyncio
from collections.abc import AsyncGenerator, Generator

import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from app.core.security import session_manager
from main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator[asyncio.AbstractEventLoop]:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
def client() -> TestClient:
    """Create a test client for the FastAPI app."""
    return TestClient(app)


@pytest.fixture
async def async_client() -> AsyncGenerator[AsyncClient]:
    """Create an async test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
def mock_session():
    """Create a mock session for testing authenticated endpoints."""
    user_info = {
        "user_id": "test_user_123",
        "email": "test@example.com",
        "name": "Test User",
        "picture": "",
        "scopes": ["https://www.googleapis.com/auth/drive.file"],
    }

    session_id = session_manager.create_session("test_user_123", user_info)

    yield {"session_id": session_id, "user_info": user_info}

    # Cleanup
    session_manager.delete_session(session_id)


@pytest.fixture
def auth_headers(mock_session):
    """Create authentication headers for testing."""
    return {"session-id": mock_session["session_id"]}


@pytest.fixture
def sample_pdf_content():
    """Sample PDF content for testing."""
    # Minimal PDF content (PDF header)
    return b"%PDF-1.4\n1 0 obj\n<<\n/Type /Catalog\n/Pages 2 0 R\n>>\nendobj\n2 0 obj\n<<\n/Type /Pages\n/Kids [3 0 R]\n/Count 1\n>>\nendobj\n3 0 obj\n<<\n/Type /Page\n/Parent 2 0 R\n/MediaBox [0 0 612 792]\n>>\nendobj\nxref\n0 4\n0000000000 65535 f \n0000000010 00000 n \n0000000079 00000 n \n0000000173 00000 n \ntrailer\n<<\n/Size 4\n/Root 1 0 R\n>>\nstartxref\n253\n%%EOF"


@pytest.fixture(autouse=True)
def cleanup_sessions():
    """Automatically cleanup sessions after each test."""
    yield
    # Clear all sessions after each test
    session_manager._sessions.clear()
    session_manager._requests.clear() if hasattr(session_manager, "_requests") else None
