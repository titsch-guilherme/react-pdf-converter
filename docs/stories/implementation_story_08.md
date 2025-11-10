# Implementation Story 08: Job Status Tracking and Real-time Updates

## Story Overview
**As a** user  
**I want** to see real-time progress updates for my PDF conversion jobs  
**So that** I can track the status of multiple files and know when they're ready for download

## SMART Criteria

### Specific
Implement job status tracking system with real-time updates, displaying conversion progress, completion status, and error information for batch file processing.

### Measurable
- ✅ `GET /api/v1/status/<job_id>` endpoint implemented
- ✅ `GET /api/v1/status` batch status endpoint implemented
- ✅ Real-time status updates in frontend (polling-based)
- ✅ Progress tracking for individual jobs (0-100%)
- ✅ Status panel displaying all user jobs
- ✅ Error handling and display for failed jobs
- ✅ Automatic status refresh for active jobs

### Achievable
Standard status tracking implementation using REST APIs and React state management with polling.

### Relevant
Essential for user experience, allowing users to monitor multiple conversion jobs simultaneously.

### Time-bound
**Estimated Duration:** 3 days  
**Sprint:** Sprint 2  
**Priority:** High (Core user experience feature)

## Technical Requirements

### Backend Components
- Job status API endpoints
- Status aggregation for batch queries
- Progress tracking integration with OCR service
- Error state management

### Frontend Components
- Status tracking hooks
- Job status display components
- Real-time polling system
- Progress indicators and error displays

## Acceptance Criteria

### AC1: Individual Job Status API
- [ ] `GET /api/v1/status/<job_id>` endpoint implemented
- [ ] Returns job status, progress, error information
- [ ] Session-based authentication required
- [ ] User can only access their own jobs
- [ ] Proper HTTP status codes for different scenarios

### AC2: Batch Status API
- [ ] `GET /api/v1/status` endpoint for all user jobs
- [ ] Returns array of job statuses for current user
- [ ] Efficient querying without N+1 problems
- [ ] Pagination support for users with many jobs
- [ ] Filtering options (active, completed, failed)

### AC3: Frontend Status Display
- [ ] Status panel showing all user jobs in table format
- [ ] Real-time updates using polling mechanism
- [ ] Individual job status indicators (pending, processing, done, failed)
- [ ] Progress bars for jobs in processing state
- [ ] Error messages displayed for failed jobs

### AC4: Real-time Updates System
- [ ] Automatic polling for active jobs every 2-3 seconds
- [ ] Polling pauses when no active jobs
- [ ] Polling resumes when new jobs are created
- [ ] Network error handling with retry logic
- [ ] Efficient polling to minimize server load

### AC5: User Experience Features
- [ ] Visual indicators for different job states
- [ ] Estimated time remaining for processing jobs
- [ ] Job completion notifications
- [ ] Ability to refresh status manually
- [ ] Clear loading states during status updates

### AC6: Error Handling and Recovery
- [ ] Network errors during status polling handled gracefully
- [ ] Failed jobs display detailed error information
- [ ] Retry options for failed jobs (future enhancement hook)
- [ ] Proper error boundaries for status components

## API Specification

### GET /api/v1/status/<job_id>
```json
Success Response (200):
{
  "job_id": "uuid-string",
  "filename": "document.pdf",
  "status": "processing",
  "progress": 65,
  "created_at": "2024-01-01T12:00:00Z",
  "updated_at": "2024-01-01T12:05:30Z",
  "download_url": null,
  "error": null,
  "estimated_completion": "2024-01-01T12:08:00Z"
}

Job Not Found (404):
{
  "error": "Job not found",
  "error_code": "JOB_NOT_FOUND"
}
```

### GET /api/v1/status
```json
Success Response (200):
{
  "jobs": [
    {
      "job_id": "uuid-1",
      "filename": "doc1.pdf",
      "status": "done",
      "progress": 100,
      "download_url": "/api/v1/download/uuid-1",
      "created_at": "2024-01-01T11:00:00Z",
      "completed_at": "2024-01-01T11:05:00Z"
    },
    {
      "job_id": "uuid-2", 
      "filename": "doc2.pdf",
      "status": "processing",
      "progress": 45,
      "estimated_completion": "2024-01-01T12:10:00Z",
      "created_at": "2024-01-01T12:00:00Z"
    },
    {
      "job_id": "uuid-3",
      "filename": "doc3.pdf", 
      "status": "failed",
      "progress": 30,
      "error": "OCR processing failed: Invalid PDF structure",
      "error_code": "OCR_PROCESSING_ERROR",
      "created_at": "2024-01-01T11:30:00Z",
      "failed_at": "2024-01-01T11:35:00Z"
    }
  ],
  "summary": {
    "total": 3,
    "pending": 0,
    "processing": 1,
    "completed": 1,
    "failed": 1
  }
}
```

## Implementation Structure

### Backend Implementation
```python
# api/v1/status.py
from fastapi import APIRouter, Depends, HTTPException
from core.security import get_current_user
from services.job_service import JobService
from models.jobs import JobStatus

router = APIRouter()

@router.get("/status/{job_id}")
async def get_job_status(
    job_id: str,
    current_user: dict = Depends(get_current_user),
    job_service: JobService = Depends()
):
    """Get status of individual job"""
    job = await job_service.get_job(job_id)
    
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    
    if job.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return {
        "job_id": job.job_id,
        "filename": job.filename,
        "status": job.status,
        "progress": job.progress,
        "created_at": job.created_at,
        "updated_at": job.updated_at,
        "download_url": job.download_url if job.status == JobStatus.DONE else None,
        "error": job.error,
        "estimated_completion": job.estimated_completion
    }

@router.get("/status")
async def get_user_jobs_status(
    current_user: dict = Depends(get_current_user),
    job_service: JobService = Depends(),
    status_filter: Optional[str] = None,
    limit: int = 50,
    offset: int = 0
):
    """Get status of all user jobs"""
    jobs = await job_service.get_user_jobs(
        current_user["user_id"],
        status_filter=status_filter,
        limit=limit,
        offset=offset
    )
    
    job_data = []
    summary = {"total": 0, "pending": 0, "processing": 0, "completed": 0, "failed": 0}
    
    for job in jobs:
        job_info = {
            "job_id": job.job_id,
            "filename": job.filename,
            "status": job.status,
            "progress": job.progress,
            "created_at": job.created_at,
            "updated_at": job.updated_at
        }
        
        if job.status == JobStatus.DONE:
            job_info["download_url"] = job.download_url
            job_info["completed_at"] = job.completed_at
            summary["completed"] += 1
        elif job.status == JobStatus.FAILED:
            job_info["error"] = job.error
            job_info["error_code"] = job.error_code
            job_info["failed_at"] = job.failed_at
            summary["failed"] += 1
        elif job.status == JobStatus.PROCESSING:
            job_info["estimated_completion"] = job.estimated_completion
            summary["processing"] += 1
        else:
            summary["pending"] += 1
            
        job_data.append(job_info)
        summary["total"] += 1
    
    return {"jobs": job_data, "summary": summary}
```

### Frontend Implementation
```typescript
// hooks/useBatchStatus.ts
import { useState, useEffect, useCallback, useRef } from 'react';
import { apiClient } from '../api/client';

interface Job {
  job_id: string;
  filename: string;
  status: 'pending' | 'processing' | 'done' | 'failed';
  progress: number;
  created_at: string;
  updated_at: string;
  download_url?: string;
  error?: string;
  error_code?: string;
  estimated_completion?: string;
}

interface JobSummary {
  total: number;
  pending: number;
  processing: number;
  completed: number;
  failed: number;
}

export const useBatchStatus = (pollingInterval: number = 3000) => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [summary, setSummary] = useState<JobSummary | null>(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [isPolling, setIsPolling] = useState(false);
  
  const pollingRef = useRef<NodeJS.Timeout | null>(null);
  const retryCountRef = useRef(0);
  const maxRetries = 3;

  const fetchJobsStatus = useCallback(async () => {
    try {
      setIsLoading(true);
      const response = await apiClient.get('/api/v1/status');
      
      setJobs(response.data.jobs);
      setSummary(response.data.summary);
      setError(null);
      retryCountRef.current = 0;
      
    } catch (err: any) {
      console.error('Failed to fetch job status:', err);
      
      if (retryCountRef.current < maxRetries) {
        retryCountRef.current++;
        setError(`Network error (retry ${retryCountRef.current}/${maxRetries})`);
      } else {
        setError('Failed to fetch job status. Please refresh manually.');
        setIsPolling(false);
      }
    } finally {
      setIsLoading(false);
    }
  }, []);

  const startPolling = useCallback(() => {
    if (pollingRef.current) return; // Already polling
    
    setIsPolling(true);
    pollingRef.current = setInterval(fetchJobsStatus, pollingInterval);
  }, [fetchJobsStatus, pollingInterval]);

  const stopPolling = useCallback(() => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
    setIsPolling(false);
  }, []);

  // Auto-start/stop polling based on active jobs
  useEffect(() => {
    const hasActiveJobs = jobs.some(job => 
      job.status === 'pending' || job.status === 'processing'
    );

    if (hasActiveJobs && !isPolling) {
      startPolling();
    } else if (!hasActiveJobs && isPolling) {
      stopPolling();
    }
  }, [jobs, isPolling, startPolling, stopPolling]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      if (pollingRef.current) {
        clearInterval(pollingRef.current);
      }
    };
  }, []);

  const refreshStatus = useCallback(() => {
    retryCountRef.current = 0;
    fetchJobsStatus();
  }, [fetchJobsStatus]);

  const addJobs = useCallback((newJobs: Job[]) => {
    setJobs(prevJobs => [...prevJobs, ...newJobs]);
  }, []);

  return {
    jobs,
    summary,
    isLoading,
    error,
    isPolling,
    refreshStatus,
    addJobs,
    startPolling,
    stopPolling
  };
};
```

### Status Display Components
```typescript
// components/status/StatusPanel.tsx
import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Chip,
  LinearProgress,
  IconButton,
  Typography,
  Box
} from '@mui/material';
import { Refresh, Download, Error } from '@mui/icons-material';
import { useBatchStatus } from '../../hooks/useBatchStatus';

export const StatusPanel: React.FC = () => {
  const { jobs, summary, isLoading, error, refreshStatus, isPolling } = useBatchStatus();

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'done': return 'success';
      case 'processing': return 'primary';
      case 'failed': return 'error';
      default: return 'default';
    }
  };

  const formatTimeAgo = (dateString: string) => {
    const date = new Date(dateString);
    const now = new Date();
    const diffMs = now.getTime() - date.getTime();
    const diffMins = Math.floor(diffMs / 60000);
    
    if (diffMins < 1) return 'Just now';
    if (diffMins < 60) return `${diffMins}m ago`;
    const diffHours = Math.floor(diffMins / 60);
    if (diffHours < 24) return `${diffHours}h ago`;
    const diffDays = Math.floor(diffHours / 24);
    return `${diffDays}d ago`;
  };

  return (
    <Paper sx={{ p: 2 }}>
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={2}>
        <Typography variant="h6">Conversion Status</Typography>
        <Box display="flex" alignItems="center" gap={1}>
          {summary && (
            <Typography variant="body2" color="text.secondary">
              {summary.total} total • {summary.processing} processing • {summary.completed} completed
            </Typography>
          )}
          <IconButton onClick={refreshStatus} disabled={isLoading}>
            <Refresh />
          </IconButton>
        </Box>
      </Box>

      {error && (
        <Box mb={2} p={1} bgcolor="error.light" borderRadius={1}>
          <Typography color="error" variant="body2">
            {error}
          </Typography>
        </Box>
      )}

      <TableContainer>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Filename</TableCell>
              <TableCell>Status</TableCell>
              <TableCell>Progress</TableCell>
              <TableCell>Created</TableCell>
              <TableCell>Actions</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {jobs.map((job) => (
              <TableRow key={job.job_id}>
                <TableCell>{job.filename}</TableCell>
                <TableCell>
                  <Chip 
                    label={job.status} 
                    color={getStatusColor(job.status)}
                    size="small"
                  />
                </TableCell>
                <TableCell>
                  {job.status === 'processing' ? (
                    <Box display="flex" alignItems="center" gap={1}>
                      <LinearProgress 
                        variant="determinate" 
                        value={job.progress} 
                        sx={{ width: 100 }}
                      />
                      <Typography variant="body2">{job.progress}%</Typography>
                    </Box>
                  ) : (
                    <Typography variant="body2">
                      {job.status === 'done' ? '100%' : job.status === 'failed' ? 'Failed' : 'Pending'}
                    </Typography>
                  )}
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {formatTimeAgo(job.created_at)}
                  </Typography>
                </TableCell>
                <TableCell>
                  {job.status === 'done' && job.download_url && (
                    <IconButton 
                      size="small" 
                      onClick={() => window.open(job.download_url, '_blank')}
                    >
                      <Download />
                    </IconButton>
                  )}
                  {job.status === 'failed' && (
                    <IconButton size="small" title={job.error}>
                      <Error color="error" />
                    </IconButton>
                  )}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {isPolling && (
        <Box mt={1} display="flex" alignItems="center" gap={1}>
          <LinearProgress sx={{ flexGrow: 1, height: 2 }} />
          <Typography variant="caption" color="text.secondary">
            Auto-refreshing...
          </Typography>
        </Box>
      )}
    </Paper>
  );
};
```

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Unit tests for status API endpoints (>90% coverage)
- [ ] Unit tests for React components and hooks
- [ ] Integration tests for polling mechanism
- [ ] E2E tests for status tracking flow
- [ ] Performance testing for batch status queries
- [ ] Code review completed and approved
- [ ] Real-time updates working smoothly

## Dependencies
- **Requires:** Implementation Story 06 (Backend File Processing)
- **Requires:** Implementation Story 07 (OCR Processing)
- **Integrates with:** Implementation Story 05 (Frontend File Upload)

## Test Scenarios

### Happy Path Tests
1. **Status Polling Flow**
   - Jobs created and polling starts automatically
   - Status updates received in real-time
   - Polling stops when all jobs complete
   - Progress bars update smoothly

2. **Batch Status Display**
   - Multiple jobs displayed correctly
   - Different status states shown properly
   - Summary information accurate
   - Actions available for appropriate states

### Error Scenarios
1. **Network Interruption**
   - Polling continues after network recovery
   - Retry mechanism works correctly
   - Error messages displayed appropriately
   - Manual refresh option available

2. **Job Failures**
   - Failed jobs displayed with error information
   - Other jobs continue processing
   - Error details accessible to user

## Performance Considerations
- [ ] Efficient polling intervals (3 seconds for active jobs)
- [ ] Batch status API optimized for multiple jobs
- [ ] Minimal re-renders during status updates
- [ ] Memory cleanup for completed jobs
- [ ] Network request optimization

## Risks and Mitigation
- **Risk:** Excessive polling causing server load
  - **Mitigation:** Intelligent polling (pause when no active jobs), rate limiting
- **Risk:** Memory leaks from polling intervals
  - **Mitigation:** Proper cleanup in useEffect, ref-based interval management
- **Risk:** Poor user experience during network issues
  - **Mitigation:** Retry logic, clear error messages, manual refresh option

## Notes
- This story implements polling-based updates as specified in the MVP approach
- WebSocket implementation can be added in future iterations
- Consider implementing push notifications for job completion
- Monitor polling frequency and server load in production