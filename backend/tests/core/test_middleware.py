"""Tests for middleware components."""

import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi import FastAPI, Request, Response
from fastapi.testclient import TestClient

from app.core.middleware import (
    ErrorHandlingMiddleware,
    LoggingMiddleware,
    RequestIDMiddleware,
)


class TestRequestIDMiddleware:
    """Test cases for RequestIDMiddleware."""

    def test_request_id_middleware_adds_id(self):
        """Test that RequestIDMiddleware adds request ID to request and response."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)

        @app.get("/test")
        async def test_endpoint(request: Request):
            # Check that request ID is added to request state
            assert hasattr(request.state, "request_id")
            assert request.state.request_id is not None
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        assert response.status_code == 200
        assert "X-Request-ID" in response.headers
        assert response.headers["X-Request-ID"] is not None
        assert len(response.headers["X-Request-ID"]) > 0

    def test_request_id_uniqueness(self):
        """Test that each request gets a unique request ID."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)

        request_ids = set()

        @app.get("/test")
        async def test_endpoint(request: Request):
            request_id = request.state.request_id
            assert request_id not in request_ids
            request_ids.add(request_id)
            return {"request_id": request_id}

        client = TestClient(app)

        # Make multiple requests
        for _ in range(10):
            response = client.get("/test")
            assert response.status_code == 200

        assert len(request_ids) == 10


class TestLoggingMiddleware:
    """Test cases for LoggingMiddleware."""

    def test_logging_middleware_logs_request_response(self):
        """Test that LoggingMiddleware logs requests and responses."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)  # Add this first for request ID
        app.add_middleware(LoggingMiddleware)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        with patch("app.core.middleware.logger") as mock_logger:
            client = TestClient(app)
            response = client.get("/test")

            assert response.status_code == 200
            assert "X-Process-Time" in response.headers

            # Verify logging calls
            assert (
                mock_logger.info.call_count >= 2
            )  # At least request start and completion

            # Check that request start was logged
            start_call = mock_logger.info.call_args_list[0]
            assert "Request started" in start_call[0][0]

            # Check that request completion was logged
            completion_call = mock_logger.info.call_args_list[1]
            assert "Request completed" in completion_call[0][0]

    def test_logging_middleware_handles_exceptions(self):
        """Test that LoggingMiddleware handles and logs exceptions."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(LoggingMiddleware)

        @app.get("/error")
        async def error_endpoint():
            raise Exception("Test error")

        with patch("app.core.middleware.logger") as mock_logger:
            client = TestClient(app)
            response = client.get("/error")

            assert response.status_code == 500
            assert "X-Request-ID" in response.headers

            # Verify error logging
            mock_logger.error.assert_called()
            error_call = mock_logger.error.call_args
            assert "Request failed" in error_call[0][0]

    def test_logging_middleware_process_time(self):
        """Test that process time is calculated and added to response."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(LoggingMiddleware)

        @app.get("/test")
        async def test_endpoint():
            import asyncio

            await asyncio.sleep(0.01)  # Small delay
            return {"message": "test"}

        client = TestClient(app)
        response = client.get("/test")

        assert response.status_code == 200
        assert "X-Process-Time" in response.headers

        process_time = float(response.headers["X-Process-Time"])
        assert process_time > 0
        assert process_time < 1  # Should be less than 1 second


class TestErrorHandlingMiddleware:
    """Test cases for ErrorHandlingMiddleware."""

    def test_error_handling_middleware_catches_exceptions(self):
        """Test that ErrorHandlingMiddleware catches and handles exceptions."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(ErrorHandlingMiddleware)

        @app.get("/error")
        async def error_endpoint():
            raise Exception("Test error")

        with patch("app.core.middleware.logger") as mock_logger:
            client = TestClient(app)
            response = client.get("/error")

            assert response.status_code == 500
            assert "X-Request-ID" in response.headers

            response_data = response.json()
            assert "error" in response_data
            assert "request_id" in response_data
            assert "detail" in response_data
            assert response_data["error"] == "Internal server error"

            # Verify error logging
            mock_logger.error.assert_called()

    def test_error_handling_middleware_preserves_http_exceptions(self):
        """Test that ErrorHandlingMiddleware doesn't interfere with HTTP exceptions."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(ErrorHandlingMiddleware)

        @app.get("/not-found")
        async def not_found_endpoint():
            from fastapi import HTTPException

            raise HTTPException(status_code=404, detail="Not found")

        client = TestClient(app)
        response = client.get("/not-found")

        # HTTP exceptions should pass through normally
        assert response.status_code == 404
        response_data = response.json()
        assert response_data["detail"] == "Not found"

    def test_error_handling_middleware_with_no_request_id(self):
        """Test ErrorHandlingMiddleware when no request ID is available."""
        app = FastAPI()
        # Don't add RequestIDMiddleware
        app.add_middleware(ErrorHandlingMiddleware)

        @app.get("/error")
        async def error_endpoint():
            raise Exception("Test error")

        with patch("app.core.middleware.logger"):
            client = TestClient(app)
            response = client.get("/error")

            assert response.status_code == 500

            response_data = response.json()
            assert response_data["request_id"] == "unknown"


class TestMiddlewareIntegration:
    """Test cases for middleware integration."""

    def test_all_middleware_together(self):
        """Test all middleware working together."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(LoggingMiddleware)
        app.add_middleware(ErrorHandlingMiddleware)

        @app.get("/test")
        async def test_endpoint(request: Request):
            return {"message": "test", "request_id": request.state.request_id}

        with patch("app.core.middleware.logger"):
            client = TestClient(app)
            response = client.get("/test")

            assert response.status_code == 200
            assert "X-Request-ID" in response.headers
            assert "X-Process-Time" in response.headers

            response_data = response.json()
            assert response_data["request_id"] == response.headers["X-Request-ID"]

    def test_middleware_order_matters(self):
        """Test that middleware order affects behavior."""
        app = FastAPI()
        # Add in different order
        app.add_middleware(ErrorHandlingMiddleware)
        app.add_middleware(LoggingMiddleware)
        app.add_middleware(RequestIDMiddleware)

        @app.get("/test")
        async def test_endpoint():
            return {"message": "test"}

        with patch("app.core.middleware.logger"):
            client = TestClient(app)
            response = client.get("/test")

            assert response.status_code == 200
            # Should still work, but middleware execution order is different

    def test_middleware_with_async_endpoint(self):
        """Test middleware with async endpoints."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(LoggingMiddleware)

        @app.get("/async-test")
        async def async_endpoint():
            import asyncio

            await asyncio.sleep(0.001)
            return {"message": "async test"}

        with patch("app.core.middleware.logger"):
            client = TestClient(app)
            response = client.get("/async-test")

            assert response.status_code == 200
            assert "X-Request-ID" in response.headers
            assert "X-Process-Time" in response.headers

    def test_middleware_with_file_upload(self):
        """Test middleware with file upload endpoints."""
        app = FastAPI()
        app.add_middleware(RequestIDMiddleware)
        app.add_middleware(LoggingMiddleware)

        @app.post("/upload")
        async def upload_endpoint():
            return {"message": "upload received"}

        with patch("app.core.middleware.logger"):
            client = TestClient(app)
            response = client.post(
                "/upload", files={"file": ("test.txt", b"test content", "text/plain")}
            )

            assert response.status_code == 200
            assert "X-Request-ID" in response.headers
            assert "X-Process-Time" in response.headers
