"""Authentication schemas."""

from datetime import datetime

from pydantic import BaseModel, Field


class TokenValidationRequest(BaseModel):
    """Request model for Google OAuth token validation."""

    access_token: str = Field(..., description="Google OAuth access token")


class UserInfo(BaseModel):
    """User information model."""

    email: str = Field(..., description="User email address")
    name: str = Field(default="", description="User display name")
    picture: str = Field(default="", description="User profile picture URL")


class SessionResponse(BaseModel):
    """Response model for successful authentication."""

    session_id: str = Field(..., description="Backend session ID")
    user_id: str = Field(..., description="Unique user identifier")
    expires_at: datetime = Field(..., description="Session expiration timestamp")
    user_info: UserInfo = Field(..., description="User information")


class ErrorResponse(BaseModel):
    """Standard error response model."""

    error: str = Field(..., description="Error message")
    detail: str | None = Field(None, description="Detailed error information")
    request_id: str | None = Field(None, description="Request ID for tracing")
