# Functional Specification

## 1. Frontend (React.js)

### 1.1. User Flow
1. **Google Drive OAuth Login:**
    - App loads login page.
    - User initiates OAuth login with Google (Drive permissions requested).
    - Only authenticated users proceed; others see error or prompt.
    - On success, user is redirected to the file conversion page.

2. **PDF Conversion Page (Multi-File):**
    - Page split vertically:
        - **Left:** Status Tracking section
            - Table/list showing all uploaded files with columns: filename, size, status (queued | processing | done | failed), and download button when ready
            - Real-time updating of file conversion statuses (polling implementation for MVP, WebSocket for future iterations)
        - **Right:** Upload section
            - Drag-and-drop zone and browse button for uploading one or multiple PDF files
            - Shows list of files selected with remove/edit options before upload
            - Start Conversion button (enabled when files are ready)
    - Each file upload creates a conversion job tracked individually
    - Status updates shown live, with download enabled upon completion
    - Option for "Upload All to Drive" after one or more conversions finish
    - Notifications/errors for individual or batch files
    - Option to logout/reauthenticate

### 1.2. Business Rules & Validations
- Only authenticate via Google OAuth (scopes: `drive.file`, `profile`, `email`).
- Only PDF files accepted, per-file max N MB (configurable, batch upload allowed).
- User must be logged in to access app features.
- Each upload triggers a backend conversion; all jobs are tracked by unique IDs.
- Conversion status/errors clearly communicated per file.
- Converted files uploaded to Google Drive within user's "Converted PDF Files" folder.

### 1.3. UI Requirements
- Responsive split-panel design (desktop and mobile)
- Use Material UI or similar for consistent look-and-feel
- Accessibility: labels, error messages, keyboard navigation
- Distinct feedback for each file (status, error, download, upload)

---

## 2. Backend (Python API)

### 2.1. API Endpoints (Multi-File Support)

#### `POST /api/v1/auth/validate`
- **Description:** Validates Google OAuth token and creates/maintains user session
- **Input:**
    - `{ "access_token": "google_oauth_token" }` JSON
- **Output:**
    - Success: `{ "session_id": "...", "user_id": "...", "expires_at": "..." }` JSON
    - Error: `{"error": "Invalid token"}` JSON + 401 status

#### `POST /api/v1/convert`
- **Description:** Accepts single or multiple PDF file uploads, performs OCR conversion on each, and returns job IDs.
- **Input:**
    - `multipart/form-data` with one or more `file` fields (array of PDFs supported)
    - `session_id` header for authentication
- **Output:**
    - Success: `{ "jobs": [ { "filename": ..., "job_id": ... }, ... ] }` JSON
    - Error: `{"error": "..."}` JSON + appropriate HTTP status
- **Rules:**
    - Validate all files (type, size, duplicates)
    - Launch separate conversion job per file (background/async)

#### `GET /api/v1/status/<job_id>`
- **Description:** Check progress of a single file conversion
- **Input:**
    - `session_id` header for authentication
- **Output:**
    - `{ "status": "pending|processing|done|failed", "progress": 0-100, "download_url": url|null, "error": null|msg }`

#### `GET /api/v1/status` (Batch status)
- **Description:** Return status for all active jobs for current user/session
- **Input:**
    - `session_id` header for authentication
- **Output:**
    - `{ "jobs": [ { "job_id": ..., "filename": ..., "status": ..., "progress": ..., "error": null|msg } ] }`
    
#### `GET /api/v1/download/<job_id>`
- **Description:** Download the converted PDF for a completed job
- **Input:**
    - `session_id` header for authentication
- **Output:**
    - PDF file (`application/pdf`), `Content-Disposition: attachment`; error otherwise

### 2.2. Authentication Flow
- Frontend obtains Google OAuth token from Google's OAuth service
- Frontend sends token to `/api/v1/auth/validate` to establish backend session
- Backend validates token with Google's token info endpoint
- Backend creates session and returns session_id for subsequent requests
- All API requests include session_id in headers for authentication
- Sessions expire after configurable timeout (default: 24 hours)

### 2.3. Security & Validation
- Accept only authenticated requests from trusted origins (CORS)
- Validate each file in multi-upload (type, size, content)
- Log all actions/errors for auditing with user/session context
- Enforce per-user limits if required
- Rate limiting per user/session

### 2.4. Batch Error Handling
- Individual file failures don't stop batch processing
- Return detailed error codes and messages per file
- Implement retry logic for transient failures (network, temporary OCR issues)
- Graceful degradation for partial batch failures
- Always remove temp files, regardless of batch job outcome
- Specific error scenarios:
  - File size/type validation errors
  - OCR processing failures
  - Network timeout recovery
  - Concurrent processing limits exceeded

### 2.5. Google Integration (Frontend)
- All Google Drive upload logic is handled client-side. Backend never directly handles user's Google credentials or Drive API calls.
- All Drive upload logic remains frontend-side, multi-file upload supported.
- Backend only validates initial OAuth token for session creation

---

## 3. Real-time Updates Strategy

### 3.1. Implementation Approach
- **MVP (Phase 1):** Polling-based status updates
  - Frontend polls `/api/v1/status` every 2-3 seconds
  - Efficient batch status endpoint reduces server load
  - Simple to implement and debug
  
- **Future Enhancement (Phase 2):** WebSocket implementation
  - Real-time status updates for better UX
  - Reduced server load from polling
  - Implementation when user base grows

### 3.2. Decision Criteria for WebSocket Migration
- More than 100 concurrent users
- Average batch size > 5 files
- User feedback indicates need for real-time updates

---

## 4. Testing Requirements

### 4.1. Batch Processing Test Cases
- **Concurrent File Processing:** Test up to N files simultaneously
- **Mixed Success/Failure Scenarios:** Some files succeed, others fail
- **File Size Limit Enforcement:** Test oversized file rejection
- **Network Interruption Recovery:** Test reconnection and status sync
- **Load Testing:** High-volume batch processing
- **Authentication Edge Cases:** Token expiry during long conversions
- **Error Propagation:** Individual file errors don't affect others

### 4.2. Security Test Cases
- Invalid session tokens
- Cross-user job access attempts
- File upload validation bypass attempts
- Rate limiting enforcement

---

## Revision History
- v1.2: Added authentication flow, API versioning, batch error handling, and testing requirements
- v1.1: Support for multi-file conversion and detailed status tracking
- v1.0: Initial specification