"""FastAPI dependencies for authentication and validation."""

from typing import Any

from fastapi import Depends, Header, HTTPException, status
from loguru import logger

from app.core.security import session_manager


async def get_session_id(
    session_id: str | None = Header(None, alias="session-id"),
) -> str:
    """Extract and validate session ID from headers."""
    if not session_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session ID required in headers",
        )
    return session_id


async def get_current_session(
    session_id: str = Depends(get_session_id),
) -> dict[str, Any]:
    """Get current session data and validate it's not expired."""
    session = session_manager.get_session(session_id)

    if not session:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired session",
        )

    return session


async def get_current_user(
    session: dict[str, Any] = Depends(get_current_session),
) -> dict[str, Any]:
    """Get current user information from session."""
    user_info = session.get("user_info", {})
    user_info["session_id"] = session.get("session_id")
    return user_info


class RateLimiter:
    """Simple in-memory rate limiter. Replace with Redis for production."""

    def __init__(self):
        self._requests: dict[str, list] = {}

    def is_allowed(self, key: str, limit: int, window_seconds: int = 60) -> bool:
        """Check if request is allowed within rate limit."""
        import time

        now = time.time()
        window_start = now - window_seconds

        # Clean old requests
        if key in self._requests:
            self._requests[key] = [
                req_time for req_time in self._requests[key] if req_time > window_start
            ]
        else:
            self._requests[key] = []

        # Check if under limit
        if len(self._requests[key]) >= limit:
            return False

        # Add current request
        self._requests[key].append(now)
        return True


# Global rate limiter instance
rate_limiter = RateLimiter()


async def check_rate_limit(
    session: dict[str, Any] = Depends(get_current_session),
) -> None:
    """Check rate limit for current user."""
    from app.core.config import settings

    user_id = session["user_id"]

    if not rate_limiter.is_allowed(
        key=f"user:{user_id}", limit=settings.RATE_LIMIT_PER_MINUTE, window_seconds=60
    ):
        logger.warning(f"Rate limit exceeded for user {user_id}")
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )
