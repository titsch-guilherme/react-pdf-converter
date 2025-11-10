# Python Code Guidelines

## **🚨 CRITICAL: Test Coverage Requirements**

### **MANDATORY TESTING STANDARDS**
- **MINIMUM 90% test coverage REQUIRED for ALL Python code**
- **ALL tests MUST pass before code can be merged**
- **NO EXCEPTIONS: Failing tests block all deployments**

### **Test Coverage Enforcement:**
```python
# pytest.ini - MANDATORY configuration
[tool:pytest]
addopts = --cov=src --cov-report=html --cov-report=term --cov-fail-under=90
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*

# Coverage configuration - NO EXCEPTIONS
[coverage:run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */settings/*

[coverage:report]
fail_under = 90    # ❌ BLOCKS DEPLOYMENT if not met
show_missing = true
skip_covered = false
```

---

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
- **✅ MANDATORY: Every module MUST have corresponding test file**

Example structure:
```
backend/
├── api/
│   ├── v1/
│   │   ├── __init__.py
│   │   ├── auth.py                    # Authentication endpoints
│   │   ├── convert.py                 # File conversion endpoints
│   │   ├── status.py                  # Job status endpoints
│   │   └── download.py                # File download endpoints
│   └── __init__.py
├── core/
│   ├── __init__.py
│   ├── config.py                      # Configuration management
│   ├── security.py                    # Authentication/session handling
│   └── dependencies.py                # FastAPI dependencies
├── services/
│   ├── __init__.py
│   ├── ocr_service.py                 # OCR processing logic
│   ├── pdf_service.py                 # PDF manipulation
│   ├── job_service.py                 # Job tracking and management
│   └── session_service.py             # Session management
├── utils/
│   ├── __init__.py
│   ├── file_utils.py                  # File validation and handling
│   └── logging_utils.py               # Logging configuration
├── models/
│   ├── __init__.py
│   ├── auth.py                        # Authentication models
│   ├── jobs.py                        # Job-related models
│   └── responses.py                   # API response models
├── config/
│   ├── __init__.py
│   └── settings.py                    # Environment settings
├── tests/                             # ✅ MANDATORY: Mirror structure
│   ├── api/
│   │   ├── v1/
│   │   │   ├── test_auth.py          # ✅ REQUIRED
│   │   │   ├── test_convert.py       # ✅ REQUIRED
│   │   │   ├── test_status.py        # ✅ REQUIRED
│   │   │   └── test_download.py      # ✅ REQUIRED
│   │   └── __init__.py
│   ├── services/
│   │   ├── test_ocr_service.py       # ✅ REQUIRED
│   │   ├── test_pdf_service.py       # ✅ REQUIRED
│   │   ├── test_job_service.py       # ✅ REQUIRED
│   │   └── test_session_service.py   # ✅ REQUIRED
│   ├── utils/
│   │   ├── test_file_utils.py        # ✅ REQUIRED
│   │   └── test_logging_utils.py     # ✅ REQUIRED
│   ├── models/
│   │   ├── test_auth.py              # ✅ REQUIRED
│   │   ├── test_jobs.py              # ✅ REQUIRED
│   │   └── test_responses.py         # ✅ REQUIRED
│   ├── core/
│   │   ├── test_config.py            # ✅ REQUIRED
│   │   ├── test_security.py          # ✅ REQUIRED
│   │   └── test_dependencies.py      # ✅ REQUIRED
│   └── conftest.py                   # Pytest configuration and fixtures
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

## 6. Automated Testing Strategy - **CRITICAL REQUIREMENTS**

### **🚨 MANDATORY Testing Standards**

#### **Test Coverage Requirements:**
- **Services:** 100% of all business logic and error paths
- **API Endpoints:** 100% of all routes and status codes
- **Models:** 100% of validation logic and edge cases
- **Utilities:** 100% of all functions and error scenarios
- **Background Tasks:** 100% of async processing and cleanup

#### **Required Test Types:**
1. **Unit Tests** (pytest)
2. **Integration Tests** (API + Database)
3. **Service Tests** (Business logic)
4. **Model Tests** (Pydantic validation)
5. **End-to-End Tests** (Full workflow)

### Test Structure
- Use `pytest` for all test types; structure `/tests` to mirror production code
- Use `pytest-asyncio` for async test support
- Use `pytest-mock` or `unittest.mock` for isolated unit tests
- Use `httpx` and FastAPI's test client for API integration tests

### **MANDATORY Testing Examples**
```python
# ✅ REQUIRED: API endpoint test with full coverage
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_batch_file_upload_success(async_client: AsyncClient, auth_headers: dict):
    """Test successful batch file upload with multiple PDFs"""
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

@pytest.mark.asyncio
async def test_batch_file_upload_validation_error(async_client: AsyncClient, auth_headers: dict):
    """Test batch upload with invalid file types"""
    files = [
        ("files", ("test1.txt", b"not_a_pdf", "text/plain")),
        ("files", ("test2.pdf", b"fake_pdf_content", "application/pdf")),
    ]
    
    response = await async_client.post(
        "/api/v1/convert",
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 400
    data = response.json()
    assert "error" in data
    assert "invalid file type" in data["error"].lower()

@pytest.mark.asyncio
async def test_batch_file_upload_unauthorized(async_client: AsyncClient):
    """Test batch upload without authentication"""
    files = [("files", ("test.pdf", b"fake_pdf", "application/pdf"))]
    
    response = await async_client.post("/api/v1/convert", files=files)
    
    assert response.status_code == 401

@pytest.mark.asyncio
async def test_batch_file_upload_file_too_large(async_client: AsyncClient, auth_headers: dict):
    """Test batch upload with oversized files"""
    large_content = b"x" * (51 * 1024 * 1024)  # 51MB file
    files = [("files", ("large.pdf", large_content, "application/pdf"))]
    
    response = await async_client.post(
        "/api/v1/convert",
        files=files,
        headers=auth_headers
    )
    
    assert response.status_code == 413

# ✅ REQUIRED: Service test with full coverage
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
    assert failed_jobs[0]["error"] == "Test error"

@pytest.mark.asyncio
async def test_job_service_concurrent_updates():
    """Test job service handles concurrent status updates"""
    job_service = JobService()
    job_id = await job_service.create_job("test.pdf", "user123")
    
    # Simulate concurrent updates
    async def update_progress(progress):
        await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=progress)
    
    # Run concurrent updates
    await asyncio.gather(
        update_progress(25),
        update_progress(50),
        update_progress(75),
        update_progress(100)
    )
    
    user_jobs = await job_service.get_user_jobs("user123")
    assert len(user_jobs) == 1
    assert user_jobs[0]["progress"] == 100

# ✅ REQUIRED: Model validation test
def test_job_model_validation():
    """Test job model validates all fields correctly"""
    from models.jobs import JobModel
    
    # Valid job
    valid_job = JobModel(
        job_id="test-123",
        filename="test.pdf",
        user_id="user123",
        status="pending",
        progress=0
    )
    assert valid_job.job_id == "test-123"
    
    # Invalid status
    with pytest.raises(ValueError):
        JobModel(
            job_id="test-123",
            filename="test.pdf",
            user_id="user123",
            status="invalid_status",
            progress=0
        )
    
    # Invalid progress
    with pytest.raises(ValueError):
        JobModel(
            job_id="test-123",
            filename="test.pdf",
            user_id="user123",
            status="pending",
            progress=150  # > 100
        )

# ✅ REQUIRED: Background task test
@pytest.mark.asyncio
async def test_pdf_conversion_background_task():
    """Test PDF conversion background task with error handling"""
    job_service = JobService()
    job_id = await job_service.create_job("test.pdf", "user123")
    
    # Mock OCR service
    with patch('services.ocr_service.convert_pdf') as mock_convert:
        mock_convert.return_value = "/tmp/converted.pdf"
        
        # Run background task
        await process_pdf_conversion(job_id, "/tmp/test.pdf", job_service)
        
        # Verify job status updated
        user_jobs = await job_service.get_user_jobs("user123")
        assert len(user_jobs) == 1
        assert user_jobs[0]["status"] == JobStatus.DONE
        assert user_jobs[0]["progress"] == 100

@pytest.mark.asyncio
async def test_pdf_conversion_background_task_error():
    """Test PDF conversion background task handles errors"""
    job_service = JobService()
    job_id = await job_service.create_job("test.pdf", "user123")
    
    # Mock OCR service to raise error
    with patch('services.ocr_service.convert_pdf') as mock_convert:
        mock_convert.side_effect = Exception("OCR processing failed")
        
        # Run background task
        await process_pdf_conversion(job_id, "/tmp/test.pdf", job_service)
        
        # Verify job status shows failure
        user_jobs = await job_service.get_user_jobs("user123")
        assert len(user_jobs) == 1
        assert user_jobs[0]["status"] == JobStatus.FAILED
        assert "OCR processing failed" in user_jobs[0]["error"]

# ✅ REQUIRED: Utility function test
def test_file_validation_utils():
    """Test file validation utility functions"""
    from utils.file_utils import validate_pdf_file, get_file_size
    
    # Test valid PDF
    with patch('builtins.open', mock_open(read_data=b'%PDF-1.4')):
        assert validate_pdf_file("/tmp/test.pdf") == True
    
    # Test invalid PDF
    with patch('builtins.open', mock_open(read_data=b'not a pdf')):
        assert validate_pdf_file("/tmp/test.txt") == False
    
    # Test file size calculation
    with patch('os.path.getsize', return_value=1024):
        assert get_file_size("/tmp/test.pdf") == 1024

# ✅ REQUIRED: Integration test
@pytest.mark.asyncio
async def test_full_conversion_workflow(async_client: AsyncClient, auth_headers: dict):
    """Test complete PDF conversion workflow end-to-end"""
    # 1. Upload file
    files = [("files", ("test.pdf", b"fake_pdf_content", "application/pdf"))]
    upload_response = await async_client.post(
        "/api/v1/convert",
        files=files,
        headers=auth_headers
    )
    assert upload_response.status_code == 200
    job_id = upload_response.json()["jobs"][0]["job_id"]
    
    # 2. Check status (should be pending initially)
    status_response = await async_client.get(
        f"/api/v1/status/{job_id}",
        headers=auth_headers
    )
    assert status_response.status_code == 200
    assert status_response.json()["status"] == "pending"
    
    # 3. Simulate processing completion
    # (In real test, you'd wait for background task or mock it)
    
    # 4. Check final status
    # 5. Download converted file
    # 6. Verify cleanup
```

### **Test Quality Gates - ENFORCED**
```python
# ✅ REQUIRED: pytest configuration
[tool:pytest]
addopts = 
    --cov=src 
    --cov-report=html 
    --cov-report=term-missing 
    --cov-fail-under=90          # ❌ BLOCKS MERGE if not met
    --strict-markers
    --disable-warnings
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests

# ✅ REQUIRED: Coverage configuration
[coverage:run]
source = src
omit = 
    */tests/*
    */venv/*
    */migrations/*
    */__pycache__/*
    */conftest.py

[coverage:report]
fail_under = 90              # ❌ BLOCKS DEPLOYMENT if not met
show_missing = true
skip_covered = false
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
```

### Test Coverage Requirements
- Target >=90% coverage (use `pytest-cov`)
- Include negative/edge-case tests (large files, malformed PDFs, etc.)
- Test error handling, security (upload validation), and rate-limiting logic
- **MANDATORY Test batch processing scenarios:**
  - Concurrent file processing
  - Mixed success/failure batches
  - Authentication during long-running jobs
  - Resource cleanup after failures
  - Memory usage with large batches
  - Database transaction rollbacks
  - Network timeout handling
  - File system error recovery

## 7. Logging & Monitoring - **ENHANCED REQUIREMENTS**

### Structured Logging
```python
# Example logging configuration with job context
from loguru import logger
import sys
from contextvars import ContextVar

# Context variables for request tracking
request_id_var: ContextVar[str] = ContextVar('request_id', default='')
user_id_var: ContextVar[str] = ContextVar('user_id', default='')
job_id_var: ContextVar[str] = ContextVar('job_id', default='')

def configure_logging():
    logger.remove()  # Remove default handler
    
    # Console logging for development
    logger.add(
        sys.stdout,
        format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | {extra[request_id]} | {extra[user_id]} | {extra[job_id]} | <level>{message}</level>",
        level="INFO",
        enqueue=True  # Thread-safe logging
    )
    
    # File logging for production
    logger.add(
        "logs/app.log",
        rotation="500 MB",
        retention="10 days",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} | {extra[request_id]} | {extra[user_id]} | {extra[job_id]} | {message}",
        level="INFO",
        enqueue=True
    )
    
    # Error logging with stack traces
    logger.add(
        "logs/errors.log",
        level="ERROR",
        rotation="100 MB",
        retention="30 days",
        backtrace=True,
        diagnose=True,
        enqueue=True
    )

# Usage with context
def log_with_context(message: str, level: str = "info"):
    """Log message with current request context"""
    logger.bind(
        request_id=request_id_var.get(),
        user_id=user_id_var.get(),
        job_id=job_id_var.get()
    ).log(level.upper(), message)

# Example usage in service
async def process_file(job_id: str, user_id: str, file_path: str):
    job_id_var.set(job_id)
    user_id_var.set(user_id)
    
    log_with_context(f"Starting file processing: {file_path}")
    
    try:
        result = await ocr_service.process_pdf(file_path)
        log_with_context(f"File processing completed successfully")
        return result
    except Exception as e:
        log_with_context(f"File processing failed: {str(e)}", "error")
        raise
```

### **Performance and Error Monitoring**
```python
# Example performance monitoring
import time
from functools import wraps
from typing import Callable, Any

def monitor_performance(func_name: str = None):
    """Decorator to monitor function performance"""
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs) -> Any:
            start_time = time.time()
            function_name = func_name or f"{func.__module__}.{func.__name__}"
            
            try:
                result = await func(*args, **kwargs)
                execution_time = time.time() - start_time
                
                log_with_context(
                    f"Performance: {function_name} completed in {execution_time:.3f}s",
                    "info"
                )
                
                # Alert if function takes too long
                if execution_time > 30:  # 30 seconds threshold
                    log_with_context(
                        f"SLOW PERFORMANCE: {function_name} took {execution_time:.3f}s",
                        "warning"
                    )
                
                return result
                
            except Exception as e:
                execution_time = time.time() - start_time
                log_with_context(
                    f"Error in {function_name} after {execution_time:.3f}s: {str(e)}",
                    "error"
                )
                raise
                
        @wraps(func)
        def sync_wrapper(*args, **kwargs) -> Any:
            # Similar implementation for sync functions
            pass
            
        return async_wrapper if asyncio.iscoroutinefunction(func) else sync_wrapper
    return decorator

# Usage
@monitor_performance("pdf_ocr_conversion")
async def convert_pdf_with_ocr(file_path: str) -> str:
    # OCR processing logic
    pass
```

## 8. Continuous Integration & Monitoring - **ENHANCED**
- Use CI tools (GitHub Actions, etc.)
- **MANDATORY:** Run lints, format checks, and full test suite on PRs/commits
- **MANDATORY:** Block merges if tests fail or coverage < 90%
- Monitor for dependency vulnerabilities (Dependabot/Snyk)
- Automated security scanning
- Performance benchmarking for conversion operations
- **NEW:** Real-time test coverage monitoring
- **NEW:** Performance regression detection
- **NEW:** Memory leak detection in long-running tests

## 9. Documentation Requirements - **ENHANCED**
- All public endpoints documented with OpenAPI (automatic with FastAPI)
- README includes:
  - Setup instructions (local, Docker, system dependencies)
  - API documentation and examples
  - **Testing procedures and coverage requirements**
  - Troubleshooting guide
  - Deployment instructions
- Code documentation with docstrings for all public functions
- Architecture decision records (ADRs) for major design choices
- **NEW:** Test coverage reports published automatically
- **NEW:** Performance benchmarking results documented

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

---

## **🚨 CRITICAL: Test Coverage Enforcement Summary**

### **Enforcement Mechanisms:**
1. **CI/CD Pipeline Blocks:** Deployments blocked if coverage < 90%
2. **Pull Request Gates:** Cannot merge without passing tests
3. **Pre-commit Hooks:** Run tests before allowing commits
4. **Daily Coverage Reports:** Team visibility on coverage trends
5. **Performance Monitoring:** Test execution time and reliability tracking
6. **Quality Gates:** Automated quality checks at every stage

### **Test Categories - ALL MANDATORY:**
- **Unit Tests:** Individual function/method testing
- **Integration Tests:** Component interaction testing
- **API Tests:** Endpoint behavior and error handling
- **Service Tests:** Business logic validation
- **Model Tests:** Data validation and serialization
- **Background Task Tests:** Async processing validation
- **Error Handling Tests:** Exception scenarios
- **Performance Tests:** Load and stress testing
- **Security Tests:** Authentication and authorization

### **Coverage Metrics Tracked:**
- **Statement Coverage:** ≥90% (no exceptions)
- **Branch Coverage:** ≥90% (no exceptions)
- **Function Coverage:** ≥90% (no exceptions)
- **Line Coverage:** ≥90% (no exceptions)
- **Test Execution Time:** < 5 minutes for full suite
- **Test Reliability:** 0% flaky tests allowed

**Remember: Test coverage is not optional. It's a fundamental requirement for code quality, reliability, and maintainability. Every line of code must be tested, every edge case must be covered, and every test must pass.**