"""API v1 router configuration."""

from fastapi import APIRouter

from app.api.v1.endpoints import auth, convert, download, status

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(convert.router, prefix="/convert", tags=["conversion"])
api_router.include_router(status.router, prefix="/status", tags=["status"])
api_router.include_router(download.router, prefix="/download", tags=["download"])
