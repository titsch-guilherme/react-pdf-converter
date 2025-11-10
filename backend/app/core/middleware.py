"""Custom middleware for logging, request tracking, and error handling."""

import time
import uuid
from collections.abc import Callable

from fastapi import Request, Response
from fastapi.responses import JSONResponse
from loguru import logger
from starlette.middleware.base import BaseHTTPMiddleware


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Add unique request ID to each request for tracing."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        # Generate unique request ID
        request_id = str(uuid.uuid4())

        # Add to request state
        request.state.request_id = request_id

        # Add to response headers
        response = await call_next(request)
        response.headers["X-Request-ID"] = request_id

        return response


class LoggingMiddleware(BaseHTTPMiddleware):
    """Log all requests and responses with structured logging."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        start_time = time.time()

        # Get request ID from state
        request_id = getattr(request.state, "request_id", "unknown")

        # Log request
        logger.info(
            "Request started",
            extra={
                "request_id": request_id,
                "method": request.method,
                "url": str(request.url),
                "client_ip": request.client.host if request.client else "unknown",
                "user_agent": request.headers.get("user-agent", "unknown"),
            },
        )

        try:
            response = await call_next(request)

            # Calculate processing time
            process_time = time.time() - start_time

            # Log response
            logger.info(
                "Request completed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "status_code": response.status_code,
                    "process_time": round(process_time, 4),
                },
            )

            # Add processing time to response headers
            response.headers["X-Process-Time"] = str(round(process_time, 4))

            return response

        except Exception as e:
            # Calculate processing time for errors
            process_time = time.time() - start_time

            # Log error
            logger.error(
                "Request failed",
                extra={
                    "request_id": request_id,
                    "method": request.method,
                    "url": str(request.url),
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "process_time": round(process_time, 4),
                },
            )

            # Return structured error response
            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "request_id": request_id,
                    "detail": "An unexpected error occurred. Please try again later.",
                },
                headers={"X-Request-ID": request_id},
            )


class ErrorHandlingMiddleware(BaseHTTPMiddleware):
    """Global error handling middleware."""

    async def dispatch(self, request: Request, call_next: Callable) -> Response:
        try:
            return await call_next(request)
        except Exception as e:
            request_id = getattr(request.state, "request_id", "unknown")

            logger.error(
                "Unhandled exception",
                extra={
                    "request_id": request_id,
                    "error": str(e),
                    "error_type": type(e).__name__,
                    "method": request.method,
                    "url": str(request.url),
                },
            )

            return JSONResponse(
                status_code=500,
                content={
                    "error": "Internal server error",
                    "request_id": request_id,
                    "detail": "An unexpected error occurred. Please try again later.",
                },
                headers={"X-Request-ID": request_id},
            )
