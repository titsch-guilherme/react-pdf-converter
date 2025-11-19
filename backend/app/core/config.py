"""Application configuration using Pydantic Settings v2."""

from typing import Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings with environment-based configuration."""

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", case_sensitive=False, extra="ignore"
    )

    # Application
    PROJECT_NAME: str = "PDF OCR Converter API"
    VERSION: str = "1.0.0"
    DESCRIPTION: str = "API for converting PDFs to searchable PDFs using OCR"
    ENVIRONMENT: str = Field(
        default="development",
        description="Environment: development, testing, production",
    )
    DEBUG: bool = Field(default=True, description="Debug mode")

    # API
    API_V1_STR: str = "/api/v1"

    # Security
    SECRET_KEY: str = Field(
        default="your-secret-key-change-in-production", min_length=32
    )
    ALLOWED_HOSTS: list[str] = Field(
        default=["*"], description="Allowed hosts for CORS"
    )

    # Session Management
    SESSION_EXPIRE_HOURS: int = Field(
        default=24, description="Session expiration in hours"
    )

    # File Processing
    MAX_FILE_SIZE_MB: int = Field(default=50, description="Maximum file size in MB")
    MAX_FILES_PER_BATCH: int = Field(
        default=10, description="Maximum files per batch upload"
    )
    UPLOAD_DIR: str = Field(
        default="uploads", description="Directory for uploaded files"
    )
    PROCESSED_DIR: str = Field(
        default="processed", description="Directory for processed files"
    )

    # Google OAuth
    GOOGLE_CLIENT_ID: str | None = Field(
        default=None, description="Google OAuth client ID"
    )
    GOOGLE_CLIENT_SECRET: str | None = Field(
        default=None, description="Google OAuth client secret"
    )

    # Logging
    LOG_LEVEL: str = Field(default="INFO", description="Logging level")
    LOG_FORMAT: str = Field(default="json", description="Log format: json or text")

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = Field(
        default=60, description="Rate limit per minute per user"
    )

    @field_validator("ENVIRONMENT")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        """Validate environment value."""
        allowed = ["development", "testing", "production"]
        if v not in allowed:
            raise ValueError(f"Environment must be one of {allowed}")
        return v

    @field_validator("LOG_LEVEL")
    @classmethod
    def validate_log_level(cls, v: str) -> str:
        """Validate log level."""
        allowed = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed:
            raise ValueError(f"Log level must be one of {allowed}")
        return v.upper()

    @field_validator("ALLOWED_HOSTS", mode="before")
    @classmethod
    def parse_allowed_hosts(cls, v: Any) -> list[str]:
        """Parse allowed hosts from string or list."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(",")]
        return v

    @property
    def is_development(self) -> bool:
        """Check if running in development mode."""
        return self.ENVIRONMENT == "development"

    @property
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.ENVIRONMENT == "production"

    @property
    def max_file_size_bytes(self) -> int:
        """Get maximum file size in bytes."""
        return self.MAX_FILE_SIZE_MB * 1024 * 1024


# Global settings instance
settings = Settings()
