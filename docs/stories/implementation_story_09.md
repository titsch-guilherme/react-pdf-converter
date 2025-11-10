# Implementation Story 09: File Download System

## Story Overview
**As a** user  
**I want** to download my converted PDF files  
**So that** I can access the searchable PDFs on my local device

## SMART Criteria

### Specific
Implement secure file download system that allows users to download their converted PDF files with proper authentication, file serving, and cleanup mechanisms.

### Measurable
- ✅ `GET /api/v1/download/<job_id>` endpoint implemented
- ✅ Secure file serving with authentication
- ✅ Proper HTTP headers for file downloads
- ✅ Download progress tracking (frontend)
- ✅ File cleanup after download expiration
- ✅ Error handling for missing or expired files
- ✅ Download links in status interface

### Achievable
Standard file download implementation using FastAPI file responses and secure file serving patterns.

### Relevant
Essential functionality allowing users to retrieve their processed files.

### Time-bound
**Estimated Duration:** 2 days  
**Sprint:** Sprint 2  
**Priority:** High (Core user functionality)

## Technical Requirements

### Backend Components
- File download endpoint with authentication
- Secure file serving mechanism
- File cleanup and expiration system
- Download logging and tracking

### Frontend Components
- Download buttons in status interface
- Download progress indication
- Error handling for download failures
- Batch download capabilities

## Acceptance Criteria

### AC1: Download Endpoint Implementation
- [ ] `GET /api/v1/download/<job_id>` endpoint implemented
- [ ] Session-based authentication required
- [ ] User can only download their own files
- [ ] Proper HTTP headers for file downloads
- [ ] Support for range requests (partial downloads)

### AC2: File Security and Access Control
- [ ] Files served only to authorized users
- [ ] Job ownership validation before download
- [ ] Secure file path handling (no directory traversal)
- [ ] Download links expire after reasonable time
- [ ] Rate limiting for download requests

### AC3: File Serving Optimization
- [ ] Efficient file streaming for large PDFs
- [ ] Proper MIME type headers
- [ ] Content-Disposition headers for filename
- [ ] Cache headers for browser optimization
- [ ] Compression support where appropriate

### AC4: Frontend Download Integration
- [ ] Download buttons in job status interface
- [ ] Download progress indication
- [ ] Error handling for failed downloads
- [ ] Success notifications for completed downloads
- [ ] Batch download functionality for multiple files

### AC5: File Management and Cleanup
- [ ] Converted files stored securely
- [ ] Automatic cleanup of old files
- [ ] Configurable file retention period
- [ ] Storage usage monitoring
- [ ] Cleanup logging and reporting

### AC6: Error Handling
- [ ] Proper error responses for missing files
- [ ] Handling of corrupted or incomplete files
- [ ] Network interruption recovery
- [ ] Clear error messages for users
- [ ] Logging of download errors

## API Specification

### GET /api/v1/download/<job_id>
```http
Request:
GET /api/v1/download/uuid-string
Headers: 
  session-id: session_identifier
  Range: bytes=0-1023 (optional)

Success Response (200):
Headers:
  Content-Type: application/pdf
  Content-Disposition: attachment; filename="converted_document.pdf"
  Content-Length: 1234567
  Accept-Ranges: bytes
  Cache-Control: private, max-age=3600
Body: [PDF file content]

Partial Content Response (206):
Headers:
  Content-Type: application/pdf
  Content-Range: bytes 0-1023/1234567
  Content-Length: 1024
Body: [Partial PDF content]

File Not Found (404):
{
  "error": "File not found or expired",
  "error_code": "FILE_NOT_FOUND"
}

Access Denied (403):
{
  "error": "Access denied",
  "error_code": "ACCESS_DENIED"
}
```

## Implementation Structure

### Backend Implementation
```python
# api/v1/download.py
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import FileResponse, StreamingResponse
from core.security import get_current_user
from services.job_service import JobService
from services.file_service import FileService
import os
import aiofiles
from typing import Optional

router = APIRouter()

@router.get("/download/{job_id}")
async def download_converted_file(
    job_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
    job_service: JobService = Depends(),
    file_service: FileService = Depends()
):
    """Download converted PDF file"""
    
    # Validate job ownership
    job = await job_service.get_job(job_id)
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    if job.status != "done" or not job.converted_path:
        raise HTTPException(status_code=404, detail="File not ready for download")
    
    # Validate file exists
    if not await file_service.file_exists(job.converted_path):
        raise HTTPException(status_code=404, detail="File not found or expired")
    
    # Log download attempt
    await file_service.log_download(job_id, current_user["user_id"])
    
    # Handle range requests for large files
    range_header = request.headers.get('Range')
    if range_header:
        return await serve_range_request(job.converted_path, job.filename, range_header)
    
    # Serve complete file
    return await serve_complete_file(job.converted_path, job.filename)

async def serve_complete_file(file_path: str, original_filename: str):
    """Serve complete file with proper headers"""
    
    file_size = os.path.getsize(file_path)
    
    def generate_file_stream():
        async def file_generator():
            async with aiofiles.open(file_path, 'rb') as file:
                while chunk := await file.read(8192):  # 8KB chunks
                    yield chunk
        return file_generator()
    
    headers = {
        'Content-Type': 'application/pdf',
        'Content-Disposition': f'attachment; filename="{original_filename}"',
        'Content-Length': str(file_size),
        'Accept-Ranges': 'bytes',
        'Cache-Control': 'private, max-age=3600'
    }
    
    return StreamingResponse(
        generate_file_stream(),
        status_code=200,
        headers=headers,
        media_type='application/pdf'
    )

async def serve_range_request(file_path: str, original_filename: str, range_header: str):
    """Handle partial content requests"""
    
    file_size = os.path.getsize(file_path)
    
    # Parse range header (e.g., "bytes=0-1023")
    try:
        range_match = re.match(r'bytes=(\d+)-(\d*)', range_header)
        if not range_match:
            raise ValueError("Invalid range format")
        
        start = int(range_match.group(1))
        end = int(range_match.group(2)) if range_match.group(2) else file_size - 1
        
        if start >= file_size or end >= file_size or start > end:
            raise ValueError("Invalid range values")
            
    except ValueError:
        raise HTTPException(status_code=416, detail="Range not satisfiable")
    
    content_length = end - start + 1
    
    def generate_range_stream():
        async def range_generator():
            async with aiofiles.open(file_path, 'rb') as file:
                await file.seek(start)
                remaining = content_length
                while remaining > 0:
                    chunk_size = min(8192, remaining)
                    chunk = await file.read(chunk_size)
                    if not chunk:
                        break
                    yield chunk
                    remaining -= len(chunk)
        return range_generator()
    
    headers = {
        'Content-Type': 'application/pdf',
        'Content-Range': f'bytes {start}-{end}/{file_size}',
        'Content-Length': str(content_length),
        'Accept-Ranges': 'bytes'
    }
    
    return StreamingResponse(
        generate_range_stream(),
        status_code=206,
        headers=headers,
        media_type='application/pdf'
    )

# services/file_service.py
class FileService:
    async def file_exists(self, file_path: str) -> bool:
        """Check if file exists and is accessible"""
        return os.path.exists(file_path) and os.path.isfile(file_path)
    
    async def log_download(self, job_id: str, user_id: str):
        """Log download activity"""
        logger.info(f"File download: job_id={job_id}, user_id={user_id}")
        # Could store in database for analytics
    
    async def cleanup_expired_files(self, retention_hours: int = 24):
        """Clean up files older than retention period"""
        cutoff_time = datetime.utcnow() - timedelta(hours=retention_hours)
        
        # Implementation depends on job storage mechanism
        # This would typically query jobs older than cutoff_time
        # and remove their associated files
        pass
```

### Frontend Implementation
```typescript
// hooks/useFileDownload.ts
import { useState, useCallback } from 'react';
import { apiClient } from '../api/client';

interface DownloadProgress {
  jobId: string;
  progress: number;
  isDownloading: boolean;
  error: string | null;
}

export const useFileDownload = () => {
  const [downloads, setDownloads] = useState<Map<string, DownloadProgress>>(new Map());

  const downloadFile = useCallback(async (jobId: string, filename: string) => {
    setDownloads(prev => new Map(prev.set(jobId, {
      jobId,
      progress: 0,
      isDownloading: true,
      error: null
    })));

    try {
      const response = await apiClient.get(`/api/v1/download/${jobId}`, {
        responseType: 'blob',
        onDownloadProgress: (progressEvent) => {
          if (progressEvent.total) {
            const progress = Math.round((progressEvent.loaded * 100) / progressEvent.total);
            setDownloads(prev => {
              const current = prev.get(jobId);
              if (current) {
                return new Map(prev.set(jobId, { ...current, progress }));
              }
              return prev;
            });
          }
        }
      });

      // Create download link and trigger download
      const blob = new Blob([response.data], { type: 'application/pdf' });
      const url = window.URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.href = url;
      link.download = filename;
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
      window.URL.revokeObjectURL(url);

      // Update download state
      setDownloads(prev => new Map(prev.set(jobId, {
        jobId,
        progress: 100,
        isDownloading: false,
        error: null
      })));

      // Clean up after delay
      setTimeout(() => {
        setDownloads(prev => {
          const newMap = new Map(prev);
          newMap.delete(jobId);
          return newMap;
        });
      }, 3000);

    } catch (error: any) {
      const errorMessage = error.response?.data?.error || 'Download failed';
      setDownloads(prev => new Map(prev.set(jobId, {
        jobId,
        progress: 0,
        isDownloading: false,
        error: errorMessage
      })));
    }
  }, []);

  const getDownloadState = useCallback((jobId: string) => {
    return downloads.get(jobId) || null;
  }, [downloads]);

  const cancelDownload = useCallback((jobId: string) => {
    setDownloads(prev => {
      const newMap = new Map(prev);
      newMap.delete(jobId);
      return newMap;
    });
  }, []);

  return {
    downloadFile,
    getDownloadState,
    cancelDownload
  };
};
```

### Download Button Component
```typescript
// components/status/DownloadButton.tsx
import React from 'react';
import {
  IconButton,
  Button,
  CircularProgress,
  Tooltip,
  Box
} from '@mui/material';
import { Download, Error } from '@mui/icons-material';
import { useFileDownload } from '../../hooks/useFileDownload';

interface DownloadButtonProps {
  jobId: string;
  filename: string;
  variant?: 'icon' | 'button';
  disabled?: boolean;
}

export const DownloadButton: React.FC<DownloadButtonProps> = ({
  jobId,
  filename,
  variant = 'icon',
  disabled = false
}) => {
  const { downloadFile, getDownloadState } = useFileDownload();
  const downloadState = getDownloadState(jobId);

  const handleDownload = () => {
    downloadFile(jobId, filename);
  };

  const isDownloading = downloadState?.isDownloading || false;
  const hasError = downloadState?.error !== null;
  const progress = downloadState?.progress || 0;

  if (variant === 'button') {
    return (
      <Button
        variant="contained"
        startIcon={hasError ? <Error /> : <Download />}
        onClick={handleDownload}
        disabled={disabled || isDownloading}
        color={hasError ? 'error' : 'primary'}
      >
        {isDownloading ? (
          <Box display="flex" alignItems="center" gap={1}>
            <CircularProgress size={16} />
            {progress}%
          </Box>
        ) : hasError ? (
          'Retry Download'
        ) : (
          'Download'
        )}
      </Button>
    );
  }

  return (
    <Tooltip title={hasError ? downloadState.error : 'Download file'}>
      <span>
        <IconButton
          onClick={handleDownload}
          disabled={disabled || isDownloading}
          color={hasError ? 'error' : 'primary'}
          size="small"
        >
          {isDownloading ? (
            <CircularProgress size={20} />
          ) : hasError ? (
            <Error />
          ) : (
            <Download />
          )}
        </IconButton>
      </span>
    </Tooltip>
  );
};
```

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Unit tests for download endpoint (>90% coverage)
- [ ] Unit tests for download components and hooks
- [ ] Integration tests for file serving
- [ ] E2E tests for download flow
- [ ] Performance testing with large files
- [ ] Security testing for access control
- [ ] Code review completed and approved

## Dependencies
- **Requires:** Implementation Story 06 (Backend File Processing)
- **Requires:** Implementation Story 07 (OCR Processing)
- **Integrates with:** Implementation Story 08 (Status Tracking)

## Test Scenarios

### Happy Path Tests
1. **Single File Download**
   - User clicks download button
   - File downloads successfully
   - Progress indicator works
   - File opens correctly

2. **Batch Download**
   - Multiple files downloaded sequentially
   - Progress tracked for each file
   - All files download successfully

3. **Large File Download**
   - Large PDF file downloads
   - Range requests work correctly
   - Download can be resumed if interrupted

### Error Scenarios
1. **File Not Found**
   - Expired or deleted file
   - Clear error message displayed
   - User can retry or refresh status

2. **Access Denied**
   - User tries to download another user's file
   - Proper 403 error returned
   - Security logged appropriately

3. **Network Interruption**
   - Download interrupted by network issue
   - User can retry download
   - Partial downloads handled correctly

## Security Considerations
- [ ] File access restricted to job owners
- [ ] Secure file path handling (no directory traversal)
- [ ] Rate limiting for download requests
- [ ] Download activity logging
- [ ] File cleanup to prevent storage exhaustion

## Performance Considerations
- [ ] Streaming responses for large files
- [ ] Range request support for partial downloads
- [ ] Efficient file serving without loading entire file into memory
- [ ] Proper caching headers
- [ ] Compression where appropriate

## File Cleanup Strategy
```python
# Background task for file cleanup
async def cleanup_expired_files():
    """Clean up files older than retention period"""
    retention_hours = settings.file_retention_hours
    cutoff_time = datetime.utcnow() - timedelta(hours=retention_hours)
    
    expired_jobs = await job_service.get_jobs_older_than(cutoff_time)
    
    for job in expired_jobs:
        if job.converted_path and os.path.exists(job.converted_path):
            try:
                os.remove(job.converted_path)
                logger.info(f"Cleaned up file: {job.converted_path}")
            except Exception as e:
                logger.error(f"Failed to cleanup file {job.converted_path}: {e}")
        
        # Update job to mark file as expired
        await job_service.mark_file_expired(job.job_id)
```

## Configuration
```python
class DownloadSettings(BaseSettings):
    file_retention_hours: int = 24
    max_download_rate: str = "10/minute"
    enable_range_requests: bool = True
    download_chunk_size: int = 8192
    max_concurrent_downloads: int = 3
```

## Risks and Mitigation
- **Risk:** Large files consuming server bandwidth
  - **Mitigation:** Rate limiting, streaming responses, range requests
- **Risk:** Storage exhaustion from accumulated files
  - **Mitigation:** Automatic cleanup, storage monitoring, retention policies
- **Risk:** Unauthorized file access
  - **Mitigation:** Strict authentication, job ownership validation, security logging

## Notes
- Consider implementing download analytics for usage insights
- Plan for CDN integration for better download performance
- Consider implementing download tokens for enhanced security
- Monitor download patterns and optimize based on usage