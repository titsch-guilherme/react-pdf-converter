"""Security utilities and authentication helpers."""

import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Any

import httpx
from loguru import logger

from app.core.config import settings


class SessionManager:
    """In-memory session manager for MVP. Replace with Redis for production."""

    def __init__(self):
        self._sessions: dict[str, dict[str, Any]] = {}

    def create_session(self, user_id: str, user_info: dict[str, Any]) -> str:
        """Create a new session and return session ID."""
        session_id = self._generate_session_id()
        expires_at = datetime.utcnow() + timedelta(hours=settings.SESSION_EXPIRE_HOURS)

        self._sessions[session_id] = {
            "user_id": user_id,
            "user_info": user_info,
            "created_at": datetime.utcnow(),
            "expires_at": expires_at,
            "last_accessed": datetime.utcnow(),
        }

        logger.info(
            f"Created session for user {user_id}", extra={"session_id": session_id}
        )
        return session_id

    def get_session(self, session_id: str) -> dict[str, Any] | None:
        """Get session data if valid and not expired."""
        if session_id not in self._sessions:
            return None

        session = self._sessions[session_id]

        # Check if session is expired
        if datetime.utcnow() > session["expires_at"]:
            self.delete_session(session_id)
            return None

        # Update last accessed time
        session["last_accessed"] = datetime.utcnow()
        return session

    def delete_session(self, session_id: str) -> bool:
        """Delete a session."""
        if session_id in self._sessions:
            user_id = self._sessions[session_id].get("user_id")
            del self._sessions[session_id]
            logger.info(
                f"Deleted session for user {user_id}", extra={"session_id": session_id}
            )
            return True
        return False

    def cleanup_expired_sessions(self) -> int:
        """Remove expired sessions and return count of removed sessions."""
        now = datetime.utcnow()
        expired_sessions = [
            session_id
            for session_id, session in self._sessions.items()
            if now > session["expires_at"]
        ]

        for session_id in expired_sessions:
            self.delete_session(session_id)

        if expired_sessions:
            logger.info(f"Cleaned up {len(expired_sessions)} expired sessions")

        return len(expired_sessions)

    def _generate_session_id(self) -> str:
        """Generate a secure session ID."""
        return secrets.token_urlsafe(32)


class GoogleOAuthValidator:
    """Google OAuth token validator."""

    GOOGLE_TOKEN_INFO_URL = "https://oauth2.googleapis.com/tokeninfo"

    async def validate_token(self, access_token: str) -> dict[str, Any] | None:
        """Validate Google OAuth access token and return user info."""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    self.GOOGLE_TOKEN_INFO_URL,
                    params={"access_token": access_token},
                    timeout=10.0,
                )

                if response.status_code != 200:
                    logger.warning(
                        f"Google token validation failed: {response.status_code}"
                    )
                    return None

                token_info = response.json()

                # Validate required fields
                required_fields = ["sub", "email", "email_verified"]
                if not all(field in token_info for field in required_fields):
                    logger.warning("Google token missing required fields")
                    return None

                # Check if email is verified
                if not token_info.get("email_verified", False):
                    logger.warning("Google account email not verified")
                    return None

                # Check if token has required scopes
                scopes = token_info.get("scope", "").split()
                required_scopes = ["https://www.googleapis.com/auth/drive.file"]
                if not any(scope in scopes for scope in required_scopes):
                    logger.warning("Google token missing required Drive scope")
                    return None

                logger.info(
                    f"Successfully validated Google token for user {token_info['email']}"
                )
                return {
                    "user_id": token_info["sub"],
                    "email": token_info["email"],
                    "name": token_info.get("name", ""),
                    "picture": token_info.get("picture", ""),
                    "scopes": scopes,
                }

        except httpx.TimeoutException:
            logger.error("Timeout validating Google token")
            return None
        except httpx.RequestError as e:
            logger.error(f"Error validating Google token: {e}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error validating Google token: {e}")
            return None


def generate_request_id() -> str:
    """Generate a unique request ID for tracing."""
    return secrets.token_hex(8)


def hash_file_content(content: bytes) -> str:
    """Generate SHA-256 hash of file content for deduplication."""
    return hashlib.sha256(content).hexdigest()


# Global instances
session_manager = SessionManager()
oauth_validator = GoogleOAuthValidator()
