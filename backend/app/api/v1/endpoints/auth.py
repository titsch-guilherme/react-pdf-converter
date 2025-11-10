"""Authentication endpoints."""

from fastapi import APIRouter, HTTPException, status
from loguru import logger

from app.core.security import oauth_validator, session_manager
from app.schemas.auth import SessionResponse, TokenValidationRequest

router = APIRouter()


@router.post("/validate", response_model=SessionResponse)
async def validate_token(request: TokenValidationRequest):
    """
    Validate Google OAuth token and create session.

    This endpoint validates the Google OAuth access token provided by the frontend
    and creates a backend session for subsequent API calls.
    """
    try:
        # Validate token with Google
        user_info = await oauth_validator.validate_token(request.access_token)

        if not user_info:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid or expired Google OAuth token",
            )

        # Create session
        session_id = session_manager.create_session(
            user_id=user_info["user_id"], user_info=user_info
        )

        # Get session data for response
        session = session_manager.get_session(session_id)

        logger.info(
            f"User authenticated successfully: {user_info['email']}",
            extra={"user_id": user_info["user_id"], "session_id": session_id},
        )

        return SessionResponse(
            session_id=session_id,
            user_id=user_info["user_id"],
            expires_at=session["expires_at"],
            user_info={
                "email": user_info["email"],
                "name": user_info.get("name", ""),
                "picture": user_info.get("picture", ""),
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during token validation: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Authentication service temporarily unavailable",
        )


@router.post("/logout")
async def logout(session_id: str):
    """
    Logout user and invalidate session.

    This endpoint invalidates the current session, effectively logging out the user.
    """
    try:
        success = session_manager.delete_session(session_id)

        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Session not found"
            )

        return {"message": "Successfully logged out"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error during logout: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Logout service temporarily unavailable",
        )
