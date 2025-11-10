# Python Code Guidelines

## 1. Project Structure
- Organize by modules: `/api`, `/services`, `/core`, `/utils`, `/models`, `/tests`, `/config`, `/logs`
    - `/api`: API endpoints (FastAPI routers) organized by version
    - `/services`: Business logic/OCR/image processing/session management
    - `/core`: Core app setup, server entry, dependency wiring
    - `/utils`: Reusable helpers/utilities
    - `/models`: Pydantic schemas/data models for requests/responses
    - `/config`: Environment/configuration files
    - `/tests`: Unit, integration, and API tests (mirrors structure of `/api`, `/services`, etc.)
    - `/logs`: App/runtime logs (gitignored)
    - `main.py`: App entry point
- Use `__init__.py` to clarify package boundaries and support modular imports.
- Example structure:

```
backend/
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py          # Authentication endpoints
│   │   ├── convert.py       # File conversion endpoints
│   │   ├── status.py        # Job status endpoints
│   │   └── download.py      # File download endpoints
│   └── __init__.py
├── core/
│   ├── __init__.py
│   ├── config.py           # Configuration management
│   ├── security.py         # Authentication/session handling
│   └── dependencies.py     # FastAPI dependencies
├── services/
│   ├── __init__.py
│   ├── ocr_service.py      # OCR processing logic
│   ├── pdf_service.py      # PDF manipulation
│   ├── job_service.py      # Job tracking and management
│   └── session_service.py  # Session management
├── utils/
│   ├── __init__.py
│   ├── file_utils.py       # File validation and handling
│   └── logging_utils.py    # Logging configuration
├── models/
│   ├── __init__.py
│   ├── auth.py            # Authentication models
│   ├── jobs.py            # Job-related models
│   └── responses.py       # API response models
├── config/
│   ├── __init__.py
│   └── settings.py        # Environment settings
├── tests/
│   ├── api/
│   │   ├── v1/
│   │   │   ├── test_auth.py
│   │   │   ├── test_convert.py
│   │   │   ├── test_status.py
│   │   │   └── test_download.py
│   │   └── __init__.py
│   ├── services/
│   │   ├── test_ocr_service.py
│   │   ├── test_job_service.py
│   │   └── test_session_service.py
│   ├── utils/
│   └── conftest.py        # Pytest configuration and fixtures
├── main.py
├── requirements.txt / pyproject.toml
└── Dockerfile
```

## 2. Dependency Management
- Use `requirements.txt` or `pyproject.toml` (prefer Poetry) for dependency and version management
- Pin versions for reproducibility; regularly update dependencies
- Use virtual environments: `venv`, `conda`, or `poetry shell`
- Ensure Dockerfile includes all binary/system dependencies (Tesseract, Poppler, etc.)
- Separate development and production dependencies

## 3. API Design & Security

### API Structure
- Use FastAPI (preferred) with typed, documented endpoints
- RESTful endpoints with clear, consistent naming and versioning (`/api/v1/`)
- Implement proper HTTP status codes and error responses
- Use Pydantic models for request/response validation
- Enable automatic OpenAPI documentation

### Authentication & Session Management
```python
# Example session management structure
from fastapi import Depends, HTTPException, Header
from typing import Optional

async def get_current_session(session_id: Optional[str] = Header(None)) -> dict:
    """Validate session and return user context"""
    if not session_id:
        raise HTTPException(status_code=401, detail="Session ID required")
    
    session = await session_service.validate_session(session_id)
    if not session:
        raise HTTPException(status_code=401, detail="Invalid session")
    
    return session
```

### Security Best Practices
- Enable/require CORS for trusted frontend domains only
- Sanitize and validate file uploads (type, size, content)
- Centralized error/exception handling; always return proper HTTP status codes
- Never store secrets in code (env vars/config only)
- Implement rate limiting per user/session
- Validate Google OAuth tokens with Google's token info endpoint
- Secure temp file handling with proper cleanup

## 4. Code Quality & Maintainability

### Code Standards
- Adhere to PEP8; use linters (`flake8`, `black`, `isort`)
- Use type hints (PEP484) for all public methods/functions
- Modular code; prefer functional separation for scalability/maintainability
- Properly document all public APIs with docstrings & OpenAPI/Swagger (built-in FastAPI)
- Use descriptive naming conventions

### Configuration Management
```python
# Example configuration structure
from pydantic import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Configuration
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_version: str = "v1"
    
    # Security
    session_secret_key: str
    session_expire_hours: int = 24
    
    # File Processing
    max_file_size_mb: int = 50
    max_concurrent_jobs: int = 10
    
    # Google OAuth
    google_client_id: str
    google_client_secret: str
    
    # Redis (for production)
    redis_url: Optional[str] = None
    
    class Config:
        env_file = ".env"

settings = Settings()
```

### Error Handling
```python
# Standardized error response format
from pydantic import BaseModel
from typing import Optional, Dict, Any

class ErrorResponse(BaseModel):
    error: str
    error_code: str
    details: Optional[Dict[str, Any]] = None

# Custom exception classes
class ValidationError(Exception):
    def __init__(self, message: str, error_code: str, details: Dict[str, Any] = None):
        self.message = message
        self.error_code = error_code
        self.details = details or {}

class ProcessingError(Exception):
    def __init__(self, message: str, error_code: str, job_id: str = None):
        self.message = message
        self.error_code = error_code
        self.job_id = job_id
```

## 5. Batch Processing & Job Management

### Job Tracking Implementation
```python
# Example job service structure
from enum import Enum
from typing import Dict, List, Optional
import asyncio
from uuid import uuid4

class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing"
    DONE = "done"
    FAILED = "failed"

class JobService:
    def __init__(self):
        self.jobs: Dict[str, Dict] = {}
    
    async def create_job(self, filename: str, user_id: str) -> str:
        job_id = str(uuid4())
        self.jobs[job_id] = {
            "job_id": job_id,
            "filename": filename,
            "user_id": user_id,
            "status": JobStatus.PENDING,
            "progress": 0,
            "error": None,
            "download_url": None,
            "created_at": datetime.utcnow()
        }
        return job_id
    
    async def update_job_status(self, job_id: str, status: JobStatus, 
                               progress: int = None, error: str = None):
        if job_id in self.jobs:
            self.jobs[job_id]["status"] = status
            if progress is not None:
                self.jobs[job_id]["progress"] = progress
            if error:
                self.jobs[job_id]["error"] = error
    
    async def get_user_jobs(self, user_id: str) -> List[Dict]:
        return [job for job in self.jobs.values() 
                if job["user_id"] == user_id]
```

### Background Task Processing
```python
# Example background task implementation
from fastapi import BackgroundTasks
import asyncio

async def process_pdf_conversion(job_id: str, file_path: str, job_service: JobService):
    """Background task for PDF conversion with proper error handling"""
    try:
        await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=10)
        
        # OCR processing with progress updates
        converted_path = await ocr_service.convert_pdf(
            file_path, 
            progress_callback=lambda p: job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=p)
        )
        
        # Generate download URL
        download_url = f"/api/v1/download/{job_id}"
        await job_service.update_job_status(job_id, JobStatus.DONE, progress=100)
        
    except Exception as e:
        await job_service.update_job_status(
            job_id, 
            JobStatus.FAILED, 
            error=f"Conversion failed: {str(e)}"
        )
    finally:
        # Cleanup temp files
        await cleanup_temp_files(file_path)
```

## 6. Automated Testing Strategy

### Test Structure
- Use `pytest` for all test types; structure `/tests` to mirror production code
- Use `pytest-asyncio` for async test support
- Use `pytest-mock` or `unittest.mock` for isolated unit tests
- Use `httpx` and FastAPI's test client for API integration tests

### Testing Examples
```python
# Example API test
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_batch_file_upload(async_client: AsyncClient, auth_headers: dict):
    """Test batch file upload with multiple PDFs"""
    files = [
        ("files", ("test1.pdf", b"fake_pdf_content_1", "application/pdf")),
        ("files", ("test2.pdf", b"fake_pdf_content_2", "application/pdf")),
    ]
    
    response = await async_client.post(
        "/api/v1/convert",
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 200
    data = response.json()
    assert "jobs" in data
    assert len(data["jobs"]) == 2
    assert all("job_id" in job for job in data["jobs"])

# Example service test
@pytest.mark.asyncio
async def test_job_service_batch_processing():
    """Test job service handles multiple concurrent jobs"""
    job_service = JobService()
    
    # Create multiple jobs
    job_ids = []
    for i in range(5):
        job_id = await job_service.create_job(f"test{i}.pdf", "user123")
        job_ids.append(job_id)
    
    # Verify all jobs created
    user_jobs = await job_service.get_user_jobs("user123")
    assert len(user_jobs) == 5
    
    # Test individual job failure doesn't affect others
    await job_service.update_job_status(job_ids[0], JobStatus.FAILED, error="Test error")
    await job_service.update_job_status(job_ids[1], JobStatus.DONE, progress=100)
    
    user_jobs = await job_service.get_user_jobs("user123")
    failed_jobs = [job for job in user_jobs if job["status"] == JobStatus.FAILED]
    done_jobs = [job for job in user_jobs if job["status"] == JobStatus.DONE]
    
    assert len(failed_jobs) == 1
    assert len(done_jobs) == 1
```

### Test Coverage Requirements
- Target >=90% coverage (use `pytest-cov`)
- Include negative/edge-case tests (large files, malformed PDFs, etc.)
- Test error handling, security (upload validation), and rate-limiting logic
- Test batch processing scenarios:
  - Concurrent file processing
  - Mixed success/failure batches
  - Authentication during long-running jobs
  - Resource cleanup after failures

## 7. Logging & Monitoring

### Structured Logging
```python
# Example logging configuration
from loguru import logger
import sys

def configure_logging():
    logger.remove()  # Remove default handler
    
    # Console logging for development
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {extra[user_id]} | {extra[job_id]} | <level>{message}</level>",
        level="INFO"
    )
    
    # File logging for production
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {extra[user_id]} | {extra[job_id]} | {message}",
        level="INFO"
    )

# Usage with context
logger = logger.bind(user_id="user123", job_id="job456")
logger.info("Starting PDF conversion")
```

## 8. Continuous Integration & Monitoring
- Use CI tools (GitHub Actions, etc.)
- Run lints, format checks, and full test suite on PRs/commits
- Monitor for dependency vulnerabilities (Dependabot/Snyk)
- Automated security scanning
- Performance benchmarking for conversion operations

## 9. Documentation Requirements
- All public endpoints documented with OpenAPI (automatic with FastAPI)
- README includes:
  - Setup instructions (local, Docker, system dependencies)
  - API documentation and examples
  - Testing procedures
  - Troubleshooting guide
  - Deployment instructions
- Code documentation with docstrings for all public functions
- Architecture decision records (ADRs) for major design choices

## 10. Production Considerations

### Performance Optimization
- Async/await for I/O operations
- Connection pooling for external services
- Efficient file handling with streaming
- Resource limits and cleanup
- Caching strategies for repeated operations

### Scalability Patterns
- Stateless service design
- Horizontal scaling support
- Load balancing considerations
- Session storage migration (in-memory → Redis)
- Background job queue (BackgroundTasks → Celery)

### Security Hardening
- Input validation and sanitization
- Rate limiting implementation
- Secure file handling
- Audit logging for security events
- Regular security updates and patches