# Architecture Guidelines

## 1. Separation of Concerns
- Maintain clear boundaries between frontend (React), backend (Python API), and third-party integrations (Tesseract, Google Drive)
- Define clear API contracts and data formats (e.g., JSON, multipart, support for batch uploads and batch status queries)
- Session-based authentication layer between frontend OAuth and backend services
- Clear separation between Google Drive operations (client-side) and PDF processing (server-side)

## 2. Security
- Use HTTPS for all data transfer
- Authenticate users via Google OAuth using secure flows with backend session validation
- Validate and sanitize all uploads; scan for malware if necessary
- Secure backend endpoints using session-based authentication
- Apply validation rules per uploaded file in batch as well as bulk operations
- Rate limiting per user/session to prevent abuse
- Secure session token generation and management
- Cross-user job access prevention

## 3. Scalability
- Design stateless, horizontally scalable services
- Support simultaneous multi-file conversions per user
- Implement job queueing, per-job status tracking, and batch download support
- Use async processing (FastAPI BackgroundTasks for MVP, Celery for production scale)
- Session storage: in-memory for development, Redis for production
- Database optional for job persistence if scale requirements grow
- Load balancing support for multiple backend instances

## 4. Maintainability
- Modular, well-documented code with strong directory separation (batch operations included)
- Favor configuration over hardcoding
- Logging should support per-job/batch tracking with user context
- Versioned API endpoints (/api/v1/) for backward compatibility
- Clear error codes and messages for debugging and user feedback

## 5. Testing and Observability
- Automated tests for both batch and single file flows
- Error monitoring/logging should include per-file job info and user context
- CI/CD must test and deploy multi-file flows as a requirement
- Load testing for concurrent users and batch processing
- Security testing for authentication and file validation
- Performance monitoring for conversion times and resource usage

## 6. Reliability
- Gracefully handle errors/timeouts per file and overall batch
- Individual file failures don't stop batch processing
- Ensure temp file cleanup works for all files in batch
- Retry logic can operate at file/job/batch level
- Session management with proper expiry and cleanup
- Fallback mechanisms for real-time updates (polling as backup for WebSocket)

## 7. Technology Stack and Dependency Management

### Frontend (React.js)
- **Node.js:** v20.x LTS
- **React:** ^18.x (latest stable)
- **react-router-dom:** ^6.x (routing)
- **@mui/material:** ^5.x (Material UI for design system)
- **@mui/icons-material:** ^5.x (Material icons)
- **react-dropzone:** ^14.x (drag-and-drop file uploads)
- **axios:** ^1.x (HTTP client with interceptors for session management)
- **google-auth-library / gapi-script:** (for Google OAuth/Drive integration; use official Google APIs)
- **react-toastify:** ^9.x (notifications & toasts)
- **dotenv:** ^16.x (environment variables in development)
- **eslint & prettier:** (for linting and formatting, latest stable)
- **jest & @testing-library/react:** (unit and integration testing)
- **cypress:** ^13.x (E2E testing)

### Backend (Python API)
- **Python:** 3.11.x (latest supported stable version)
- **FastAPI:** ^0.111.x (or latest stable) — recommended for async & OpenAPI docs
- **uvicorn:** ^0.30.x (ASGI server)
- **pytesseract:** ^0.3.x (Python bindings for Tesseract)
- **pdf2image:** ^1.17.x (PDF to image conversion)
- **Pillow:** ^10.3.x (image processing)
- **PyPDF2:** ^3.0.x (PDF manipulation)
- **reportlab:** ^4.3.x (PDF creation/merging, if needed)
- **python-multipart:** ^0.0.9 (file uploads)
- **aiofiles:** ^23.2.x (async file operations)
- **python-dotenv:** ^1.0.x (environment variables)
- **httpx:** ^0.27.x (async HTTP requests for Google token validation)
- **pytest:** ^7.x (testing framework)
- **pytest-asyncio:** ^0.21.x (async testing support)
- **pytest-cov:** ^4.x (coverage reporting)
- **flake8, black, isort:** (linting, formatting)
- **loguru:** ^0.7.x (structured logging)
- **slowapi:** ^0.1.x (rate limiting for FastAPI)
- **redis:** ^4.x (session storage for production)

### System Dependencies
- **Tesseract OCR:** Latest stable release (system package, e.g., tesseract-ocr)
- **Poppler utils:** For pdf2image backend (system package, e.g., poppler-utils)

## 8. API Design Standards

### Versioning Strategy
- All API endpoints use `/api/v1/` prefix
- Maintain backward compatibility within major versions
- Clear migration path for version upgrades

### Authentication Pattern
- Session-based authentication with Google OAuth token validation
- Consistent session_id header for all authenticated endpoints
- Proper error responses for authentication failures

### Error Response Format
```json
{
  "error": "descriptive_error_message",
  "error_code": "SPECIFIC_ERROR_CODE",
  "details": {
    "field": "additional_context"
  }
}
```

### Batch Operation Standards
- Consistent job tracking with unique job_id per file
- Standardized status values: pending, processing, done, failed
- Progress reporting (0-100) where applicable
- Individual error reporting within batch operations

## 9. Real-time Updates Architecture

### Implementation Strategy
- **Phase 1 (MVP):** HTTP polling every 2-3 seconds
  - Simple to implement and debug
  - Efficient batch status endpoint
  - Automatic pause/resume based on job states
  
- **Phase 2:** WebSocket implementation
  - Real-time status updates
  - Fallback to polling if WebSocket fails
  - Server-sent events as alternative

### Migration Criteria
- More than 100 concurrent users
- Average batch size > 5 files
- User feedback indicates need for real-time updates

## 10. Dependency Update & Monitoring Policy
- Use Dependabot or Renovate for dependency update tracking in both backend and frontend
- Regularly review changelogs for major, potentially breaking releases
- Schedule quarterly reviews of stack versions and plan upgrade paths in advance
- Security vulnerability scanning with Snyk or similar tools

## 11. Additional Tooling
- **Docker:** Latest stable for consistent dev/test/prod environments
- **Docker Compose:** For local full-stack development
- **GitHub Actions:** CI/CD for automatic builds/tests/deployment
- **Pre-commit hooks:** For linting & formatting enforcement
- **Snyk or similar:** For dependency vulnerability scanning

## 12. Performance and Monitoring

### Logging Standards
- Structured logging with user/session/job context
- Performance metrics for conversion operations
- Error tracking with full context for debugging
- Audit trail for security-sensitive operations

### Metrics to Monitor
- API response times and error rates
- Conversion success/failure rates by file type/size
- Concurrent user and job counts
- Resource utilization (CPU, memory, disk)
- Session management metrics

---

This architecture emphasizes maintainability, security, and scalability while providing clear guidelines for implementation teams. The phased approach allows for MVP delivery while planning for future enhancements based on user feedback and growth requirements.