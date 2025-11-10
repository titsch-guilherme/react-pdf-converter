# Implementation Story 06: Backend File Processing and Job Management

## Story Overview
**As a** backend system  
**I want** to receive, validate, and process multiple PDF files for OCR conversion  
**So that** I can manage conversion jobs and track their progress individually

## SMART Criteria

### Specific
Implement backend endpoints for file upload, validation, job creation, and background processing management for PDF OCR conversion.

### Measurable
- ✅ `POST /api/v1/convert` endpoint for batch file upload
- ✅ File validation and sanitization system
- ✅ Job creation and tracking system
- ✅ Background task processing framework
- ✅ File storage and cleanup management
- ✅ Error handling for individual file failures
- ✅ Progress tracking and status updates

### Achievable
Standard file processing implementation using FastAPI, background tasks, and job management patterns.

### Relevant
Core backend functionality required for PDF conversion service.

### Time-bound
**Estimated Duration:** 4 days  
**Sprint:** Sprint 2  
**Priority:** High (Core backend functionality)

## Technical Requirements

### Dependencies
- `python-multipart` for file uploads
- `aiofiles` for async file operations
- `uuid` for job ID generation
- Background task processing (FastAPI BackgroundTasks)
- File validation utilities

### System Requirements
- Temporary file storage for uploaded PDFs
- Job status tracking (in-memory for MVP)
- File cleanup mechanisms
- Error isolation for batch processing

## Acceptance Criteria

### AC1: File Upload Endpoint
- [ ] `POST /api/v1/convert` accepts multipart/form-data
- [ ] Multiple files supported in single request
- [ ] Session-based authentication required
- [ ] File validation performed on upload
- [ ] Unique job ID generated per file

### AC2: File Validation System
- [ ] PDF file type validation (MIME type and magic bytes)
- [ ] File size validation with configurable limits
- [ ] File structure validation (basic PDF integrity)
- [ ] Malicious file detection (basic security checks)
- [ ] Duplicate file handling within batch

### AC3: Job Management System
- [ ] Unique job ID generation for each file
- [ ] Job status tracking (pending, processing, done, failed)
- [ ] Progress percentage tracking (0-100)
- [ ] Error message storage for failed jobs
- [ ] User association for job isolation

### AC4: Background Processing
- [ ] Asynchronous job processing using FastAPI BackgroundTasks
- [ ] Individual file processing isolation
- [ ] Progress updates during processing
- [ ] Error handling without affecting other jobs
- [ ] Resource cleanup after processing

### AC5: File Storage Management
- [ ] Secure temporary file storage
- [ ] Unique file naming to prevent conflicts
- [ ] Automatic cleanup of temporary files
- [ ] Converted file storage for download
- [ ] Storage quota management per user

### AC6: Error Handling and Resilience
- [ ] Individual file failures don't stop batch processing
- [ ] Detailed error reporting per job
- [ ] Retry mechanisms for transient failures
- [ ] Graceful handling of system resource limits
- [ ] Proper HTTP status codes and error responses

## API Specification

### POST /api/v1/convert
```json
Request:
Content-Type: multipart/form-data
Headers: session-id: {session_id}
Body: files[] (multiple PDF files)

Success Response (200):
{
  "jobs": [
    {
      "job_id": "uuid-string",
      "filename": "document1.pdf",
      "status": "pending",
      "created_at": "2024-01-01T12:00:00Z"
    },
    {
      "job_id": "uuid-string", 
      "filename": "document2.pdf",
      "status": "pending",
      "created_at": "2024-01-01T12:00:00Z"
    }
  ]
}

Partial Success Response (207):
{
  "jobs": [
    {
      "job_id": "uuid-string",
      "filename": "document1.pdf", 
      "status": "pending"
    }
  ],
  "errors": [
    {
      "filename": "invalid.txt",
      "error": "Invalid file type",
      "error_code": "INVALID_FILE_TYPE"
    }
  ]
}

Error Response (400):
{
  "error": "No valid files provided",
  "error_code": "NO_VALID_FILES"
}
```

## Implementation Structure

### Core Components
```python
# models/jobs.py
class JobStatus(str, Enum):
    PENDING = "pending"
    PROCESSING = "processing" 
    DONE = "done"
    FAILED = "failed"

class Job(BaseModel):
    job_id: str
    filename: str
    user_id: str
    status: JobStatus
    progress: int = 0
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    file_path: Optional[str] = None
    converted_path: Optional[str] = None

# services/job_service.py
class JobService:
    async def create_job(self, filename: str, user_id: str, file_path: str) -> Job
    async def update_job_status(self, job_id: str, status: JobStatus, progress: int = None, error: str = None)
    async def get_job(self, job_id: str) -> Optional[Job]
    async def get_user_jobs(self, user_id: str) -> List[Job]
    async def cleanup_completed_jobs(self, older_than_hours: int = 24)

# services/file_service.py
class FileService:
    async def validate_file(self, file: UploadFile) -> ValidationResult
    async def save_uploaded_file(self, file: UploadFile, job_id: str) -> str
    async def cleanup_temp_files(self, file_paths: List[str])
    def generate_unique_filename(self, original_name: str, job_id: str) -> str
```

### Background Processing
```python
# services/conversion_service.py
async def process_pdf_conversion(job_id: str, file_path: str, job_service: JobService):
    """Background task for PDF OCR conversion"""
    try:
        await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=10)
        
        # Placeholder for OCR processing (implemented in next story)
        # This will be replaced with actual OCR conversion
        await simulate_conversion_process(job_id, file_path, job_service)
        
        await job_service.update_job_status(job_id, JobStatus.DONE, progress=100)
        
    except Exception as e:
        error_msg = f"Conversion failed: {str(e)}"
        await job_service.update_job_status(job_id, JobStatus.FAILED, error=error_msg)
    finally:
        # Cleanup will be handled by separate cleanup service
        pass

async def simulate_conversion_process(job_id: str, file_path: str, job_service: JobService):
    """Simulate conversion process with progress updates"""
    for progress in [25, 50, 75, 90]:
        await asyncio.sleep(1)  # Simulate processing time
        await job_service.update_job_status(job_id, JobStatus.PROCESSING, progress=progress)
```

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Unit tests for all file processing components (>90% coverage)
- [ ] Integration tests for file upload and job creation
- [ ] API tests for all endpoints
- [ ] Error scenario testing completed
- [ ] Performance testing for batch uploads
- [ ] Security testing for file validation
- [ ] Code review completed and approved

## Dependencies
- **Requires:** Implementation Story 02 (Backend Bootstrap)
- **Requires:** Implementation Story 04 (Backend Authentication)
- **Integrates with:** Implementation Story 05 (Frontend File Upload)
- **Prepares for:** Implementation Story 07 (OCR Processing)

## Test Scenarios

### Happy Path Tests
1. **Single File Upload**
   - Valid PDF file uploaded
   - Job created successfully
   - Background processing started
   - Status updates correctly

2. **Batch File Upload**
   - Multiple PDF files uploaded
   - Individual jobs created for each file
   - All jobs processed independently
   - Correct status tracking

3. **File Validation Success**
   - Valid PDF files pass validation
   - Jobs created for valid files
   - Processing initiated correctly

### Error Scenarios
1. **Invalid File Types**
   - Non-PDF files rejected
   - Appropriate error messages
   - Valid files still processed
   - Partial success response

2. **File Size Exceeded**
   - Oversized files rejected
   - Error details provided
   - Other files continue processing

3. **Processing Failures**
   - Individual job failures isolated
   - Error messages captured
   - Other jobs continue processing
   - Proper cleanup performed

## File Validation Rules
```python
async def validate_pdf_file(file: UploadFile) -> ValidationResult:
    """Comprehensive PDF file validation"""
    
    # Check file size
    if file.size > MAX_FILE_SIZE:
        return ValidationResult(
            valid=False, 
            error=f"File size exceeds {MAX_FILE_SIZE} bytes limit",
            error_code="FILE_TOO_LARGE"
        )
    
    # Check MIME type
    if file.content_type != "application/pdf":
        return ValidationResult(
            valid=False,
            error="Invalid file type. Only PDF files are allowed",
            error_code="INVALID_FILE_TYPE"
        )
    
    # Check file extension
    if not file.filename.lower().endswith('.pdf'):
        return ValidationResult(
            valid=False,
            error="Invalid file extension. Only .pdf files are allowed", 
            error_code="INVALID_FILE_EXTENSION"
        )
    
    # Basic PDF structure validation
    content = await file.read(1024)  # Read first 1KB
    await file.seek(0)  # Reset file pointer
    
    if not content.startswith(b'%PDF-'):
        return ValidationResult(
            valid=False,
            error="Invalid PDF file structure",
            error_code="INVALID_PDF_STRUCTURE"
        )
    
    return ValidationResult(valid=True)
```

## Security Considerations
- [ ] File upload size limits enforced
- [ ] File type validation with magic byte checking
- [ ] Secure temporary file storage with proper permissions
- [ ] User isolation for file access
- [ ] Input sanitization for filenames
- [ ] Rate limiting for upload endpoints

## Performance Considerations
- [ ] Async file operations to prevent blocking
- [ ] Efficient file validation without loading entire file
- [ ] Background task processing for scalability
- [ ] Memory-efficient file handling
- [ ] Proper resource cleanup and garbage collection

## Configuration
```python
class FileProcessingSettings(BaseSettings):
    max_file_size: int = 50 * 1024 * 1024  # 50MB
    max_files_per_batch: int = 10
    upload_dir: str = "/tmp/pdf_uploads"
    converted_dir: str = "/tmp/pdf_converted"
    cleanup_interval_hours: int = 24
    max_concurrent_jobs: int = 5
```

## Risks and Mitigation
- **Risk:** Large file uploads consuming server resources
  - **Mitigation:** File size limits, streaming uploads, resource monitoring
- **Risk:** Malicious file uploads
  - **Mitigation:** Comprehensive validation, sandboxed processing, virus scanning
- **Risk:** Storage space exhaustion
  - **Mitigation:** Automatic cleanup, storage quotas, monitoring

## Notes
- This story focuses on job management and file handling infrastructure
- Actual OCR processing will be implemented in the next story
- Consider implementing file chunking for very large uploads in future iterations
- Plan for horizontal scaling with shared file storage