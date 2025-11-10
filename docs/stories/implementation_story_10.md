# Implementation Story 10: Google Drive Integration

## Story Overview
**As a** user  
**I want** to upload my converted PDF files directly to my Google Drive  
**So that** I can store them in my cloud storage without manual download and upload

## SMART Criteria

### Specific
Implement Google Drive integration that allows users to upload converted PDF files directly to their Google Drive in a dedicated "Converted PDF Files" folder.

### Measurable
- ✅ Google Drive API integration functional
- ✅ Folder creation and management in Google Drive
- ✅ Individual file upload to Drive capability
- ✅ Batch upload functionality for multiple files
- ✅ Upload progress tracking and status updates
- ✅ Error handling for Drive API failures
- ✅ User interface for Drive upload actions

### Achievable
Standard Google Drive API integration using official Google APIs and established patterns.

### Relevant
Provides seamless cloud storage integration, enhancing user workflow and file management.

### Time-bound
**Estimated Duration:** 4 days  
**Sprint:** Sprint 3  
**Priority:** High (Key differentiating feature)

## Technical Requirements

### Google Drive API
- Drive API v3 for file operations
- OAuth 2.0 with drive.file scope
- Folder management and file upload
- Progress tracking for uploads

### Frontend Integration
- Google Drive service class
- Upload progress components
- Batch upload management
- Error handling and retry logic

## Acceptance Criteria

### AC1: Google Drive Service Setup
- [ ] Google Drive API client configured
- [ ] OAuth token management for Drive operations
- [ ] Drive API permissions validated (drive.file scope)
- [ ] Error handling for API authentication failures
- [ ] Rate limiting compliance with Google's limits

### AC2: Folder Management
- [ ] "Converted PDF Files" folder created automatically
- [ ] Folder existence check before file uploads
- [ ] Folder creation with proper permissions
- [ ] Handling of existing folder scenarios
- [ ] Folder ID caching for performance

### AC3: Individual File Upload
- [ ] Single file upload to Google Drive
- [ ] Progress tracking during upload
- [ ] Success confirmation with Drive file ID
- [ ] Error handling for upload failures
- [ ] Retry mechanism for failed uploads

### AC4: Batch Upload Functionality
- [ ] Multiple files uploaded simultaneously
- [ ] Individual progress tracking per file
- [ ] Overall batch progress indication
- [ ] Partial success handling (some files succeed, others fail)
- [ ] Batch operation cancellation capability

### AC5: User Interface Integration
- [ ] Upload to Drive buttons in status interface
- [ ] Batch "Upload All to Drive" functionality
- [ ] Upload progress indicators
- [ ] Success/failure notifications
- [ ] Drive upload status in job tracking

### AC6: Error Handling and Recovery
- [ ] Network error handling with retry logic
- [ ] Google API quota exceeded handling
- [ ] Invalid token refresh handling
- [ ] File size limit error handling
- [ ] Clear error messages for users

## Implementation Structure

### Google Drive Service
```typescript
// services/googleDriveService.ts
class GoogleDriveService {
  private accessToken: string;
  private folderCache: Map<string, string> = new Map();

  constructor(accessToken: string) {
    this.accessToken = accessToken;
  }

  async ensureConvertedFilesFolder(): Promise<string> {
    const folderName = 'Converted PDF Files';
    
    // Check cache first
    if (this.folderCache.has(folderName)) {
      return this.folderCache.get(folderName)!;
    }

    try {
      // Search for existing folder
      const searchResponse = await this.searchFiles({
        q: `name='${folderName}' and mimeType='application/vnd.google-apps.folder' and trashed=false`,
        fields: 'files(id, name)'
      });

      let folderId: string;

      if (searchResponse.files && searchResponse.files.length > 0) {
        folderId = searchResponse.files[0].id;
      } else {
        // Create new folder
        const createResponse = await this.createFolder(folderName);
        folderId = createResponse.id;
      }

      this.folderCache.set(folderName, folderId);
      return folderId;

    } catch (error) {
      throw new Error(`Failed to ensure folder exists: ${error.message}`);
    }
  }

  async uploadFile(
    file: Blob, 
    filename: string, 
    onProgress?: (progress: number) => void
  ): Promise<DriveUploadResult> {
    try {
      const folderId = await this.ensureConvertedFilesFolder();
      
      const metadata = {
        name: filename,
        parents: [folderId]
      };

      const form = new FormData();
      form.append('metadata', new Blob([JSON.stringify(metadata)], {
        type: 'application/json'
      }));
      form.append('file', file);

      const xhr = new XMLHttpRequest();
      
      return new Promise((resolve, reject) => {
        xhr.upload.addEventListener('progress', (event) => {
          if (event.lengthComputable && onProgress) {
            const progress = Math.round((event.loaded / event.total) * 100);
            onProgress(progress);
          }
        });

        xhr.addEventListener('load', () => {
          if (xhr.status === 200) {
            const response = JSON.parse(xhr.responseText);
            resolve({
              success: true,
              fileId: response.id,
              webViewLink: response.webViewLink
            });
          } else {
            reject(new Error(`Upload failed: ${xhr.statusText}`));
          }
        });

        xhr.addEventListener('error', () => {
          reject(new Error('Network error during upload'));
        });

        xhr.open('POST', 'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart');
        xhr.setRequestHeader('Authorization', `Bearer ${this.accessToken}`);
        xhr.send(form);
      });

    } catch (error) {
      return {
        success: false,
        error: error.message
      };
    }
  }

  async uploadMultipleFiles(
    files: Array<{ blob: Blob; filename: string; jobId: string }>,
    onProgress?: (jobId: string, progress: number) => void,
    onComplete?: (jobId: string, result: DriveUploadResult) => void
  ): Promise<BatchUploadResult> {
    const results: Map<string, DriveUploadResult> = new Map();
    const uploadPromises = files.map(async ({ blob, filename, jobId }) => {
      try {
        const result = await this.uploadFile(
          blob, 
          filename, 
          (progress) => onProgress?.(jobId, progress)
        );
        results.set(jobId, result);
        onComplete?.(jobId, result);
        return { jobId, result };
      } catch (error) {
        const errorResult: DriveUploadResult = {
          success: false,
          error: error.message
        };
        results.set(jobId, errorResult);
        onComplete?.(jobId, errorResult);
        return { jobId, result: errorResult };
      }
    });

    await Promise.allSettled(uploadPromises);

    const successful = Array.from(results.values()).filter(r => r.success).length;
    const failed = results.size - successful;

    return {
      total: results.size,
      successful,
      failed,
      results
    };
  }

  private async searchFiles(params: any): Promise<any> {
    const url = new URL('https://www.googleapis.com/drive/v3/files');
    Object.keys(params).forEach(key => url.searchParams.append(key, params[key]));

    const response = await fetch(url.toString(), {
      headers: {
        'Authorization': `Bearer ${this.accessToken}`
      }
    });

    if (!response.ok) {
      throw new Error(`Drive API error: ${response.statusText}`);
    }

    return response.json();
  }

  private async createFolder(name: string): Promise<any> {
    const response = await fetch('https://www.googleapis.com/drive/v3/files', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${this.accessToken}`,
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name,
        mimeType: 'application/vnd.google-apps.folder'
      })
    });

    if (!response.ok) {
      throw new Error(`Failed to create folder: ${response.statusText}`);
    }

    return response.json();
  }
}

// Types
interface DriveUploadResult {
  success: boolean;
  fileId?: string;
  webViewLink?: string;
  error?: string;
}

interface BatchUploadResult {
  total: number;
  successful: number;
  failed: number;
  results: Map<string, DriveUploadResult>;
}
```

### Drive Upload Hook
```typescript
// hooks/useDriveUpload.ts
import { useState, useCallback } from 'react';
import { GoogleDriveService } from '../services/googleDriveService';
import { useAuth } from '../context/AuthContext';

interface DriveUploadState {
  jobId: string;
  progress: number;
  status: 'idle' | 'uploading' | 'success' | 'error';
  error?: string;
  driveFileId?: string;
}

export const useDriveUpload = () => {
  const { user } = useAuth();
  const [uploadStates, setUploadStates] = useState<Map<string, DriveUploadState>>(new Map());

  const uploadToDrive = useCallback(async (jobId: string, filename: string) => {
    if (!user?.accessToken) {
      throw new Error('Not authenticated with Google');
    }

    // Initialize upload state
    setUploadStates(prev => new Map(prev.set(jobId, {
      jobId,
      progress: 0,
      status: 'uploading'
    })));

    try {
      // Download file from backend
      const response = await fetch(`/api/v1/download/${jobId}`, {
        headers: {
          'session-id': user.sessionId
        }
      });

      if (!response.ok) {
        throw new Error('Failed to download file for Drive upload');
      }

      const blob = await response.blob();
      
      // Upload to Google Drive
      const driveService = new GoogleDriveService(user.accessToken);
      const result = await driveService.uploadFile(
        blob,
        filename,
        (progress) => {
          setUploadStates(prev => {
            const current = prev.get(jobId);
            if (current) {
              return new Map(prev.set(jobId, { ...current, progress }));
            }
            return prev;
          });
        }
      );

      if (result.success) {
        setUploadStates(prev => new Map(prev.set(jobId, {
          jobId,
          progress: 100,
          status: 'success',
          driveFileId: result.fileId
        })));
      } else {
        throw new Error(result.error || 'Upload failed');
      }

    } catch (error: any) {
      setUploadStates(prev => new Map(prev.set(jobId, {
        jobId,
        progress: 0,
        status: 'error',
        error: error.message
      })));
    }
  }, [user]);

  const uploadMultipleToDrive = useCallback(async (
    jobs: Array<{ jobId: string; filename: string }>
  ) => {
    if (!user?.accessToken) {
      throw new Error('Not authenticated with Google');
    }

    // Initialize all upload states
    jobs.forEach(({ jobId }) => {
      setUploadStates(prev => new Map(prev.set(jobId, {
        jobId,
        progress: 0,
        status: 'uploading'
      })));
    });

    try {
      // Download all files
      const filePromises = jobs.map(async ({ jobId, filename }) => {
        const response = await fetch(`/api/v1/download/${jobId}`, {
          headers: {
            'session-id': user.sessionId
          }
        });
        
        if (!response.ok) {
          throw new Error(`Failed to download ${filename}`);
        }
        
        const blob = await response.blob();
        return { blob, filename, jobId };
      });

      const files = await Promise.all(filePromises);

      // Upload to Google Drive
      const driveService = new GoogleDriveService(user.accessToken);
      await driveService.uploadMultipleFiles(
        files,
        (jobId, progress) => {
          setUploadStates(prev => {
            const current = prev.get(jobId);
            if (current) {
              return new Map(prev.set(jobId, { ...current, progress }));
            }
            return prev;
          });
        },
        (jobId, result) => {
          setUploadStates(prev => new Map(prev.set(jobId, {
            jobId,
            progress: result.success ? 100 : 0,
            status: result.success ? 'success' : 'error',
            error: result.error,
            driveFileId: result.fileId
          })));
        }
      );

    } catch (error: any) {
      // Mark all as failed
      jobs.forEach(({ jobId }) => {
        setUploadStates(prev => new Map(prev.set(jobId, {
          jobId,
          progress: 0,
          status: 'error',
          error: error.message
        })));
      });
    }
  }, [user]);

  const getUploadState = useCallback((jobId: string) => {
    return uploadStates.get(jobId);
  }, [uploadStates]);

  const clearUploadState = useCallback((jobId: string) => {
    setUploadStates(prev => {
      const newMap = new Map(prev);
      newMap.delete(jobId);
      return newMap;
    });
  }, []);

  return {
    uploadToDrive,
    uploadMultipleToDrive,
    getUploadState,
    clearUploadState
  };
};
```

### Drive Upload Components
```typescript
// components/drive/DriveUploadButton.tsx
import React from 'react';
import {
  Button,
  IconButton,
  CircularProgress,
  Tooltip,
  Box
} from '@mui/material';
import { CloudUpload, CheckCircle, Error } from '@mui/icons-material';
import { useDriveUpload } from '../../hooks/useDriveUpload';

interface DriveUploadButtonProps {
  jobId: string;
  filename: string;
  variant?: 'icon' | 'button';
  disabled?: boolean;
}

export const DriveUploadButton: React.FC<DriveUploadButtonProps> = ({
  jobId,
  filename,
  variant = 'icon',
  disabled = false
}) => {
  const { uploadToDrive, getUploadState } = useDriveUpload();
  const uploadState = getUploadState(jobId);

  const handleUpload = () => {
    uploadToDrive(jobId, filename);
  };

  const isUploading = uploadState?.status === 'uploading';
  const isSuccess = uploadState?.status === 'success';
  const hasError = uploadState?.status === 'error';
  const progress = uploadState?.progress || 0;

  const getIcon = () => {
    if (isSuccess) return <CheckCircle color="success" />;
    if (hasError) return <Error color="error" />;
    if (isUploading) return <CircularProgress size={20} />;
    return <CloudUpload />;
  };

  const getTooltip = () => {
    if (isSuccess) return 'Uploaded to Google Drive';
    if (hasError) return uploadState?.error || 'Upload failed';
    if (isUploading) return `Uploading... ${progress}%`;
    return 'Upload to Google Drive';
  };

  if (variant === 'button') {
    return (
      <Button
        variant="outlined"
        startIcon={getIcon()}
        onClick={handleUpload}
        disabled={disabled || isUploading || isSuccess}
        color={hasError ? 'error' : isSuccess ? 'success' : 'primary'}
      >
        {isUploading ? (
          <Box display="flex" alignItems="center" gap={1}>
            Uploading... {progress}%
          </Box>
        ) : isSuccess ? (
          'Uploaded'
        ) : hasError ? (
          'Retry Upload'
        ) : (
          'Upload to Drive'
        )}
      </Button>
    );
  }

  return (
    <Tooltip title={getTooltip()}>
      <span>
        <IconButton
          onClick={handleUpload}
          disabled={disabled || isUploading || isSuccess}
          color={hasError ? 'error' : isSuccess ? 'success' : 'primary'}
          size="small"
        >
          {getIcon()}
        </IconButton>
      </span>
    </Tooltip>
  );
};

// components/drive/BatchDriveUpload.tsx
export const BatchDriveUpload: React.FC<{ jobs: Job[] }> = ({ jobs }) => {
  const { uploadMultipleToDrive } = useDriveUpload();
  const [isUploading, setIsUploading] = useState(false);

  const completedJobs = jobs.filter(job => job.status === 'done');
  const canUpload = completedJobs.length > 0 && !isUploading;

  const handleBatchUpload = async () => {
    setIsUploading(true);
    try {
      await uploadMultipleToDrive(
        completedJobs.map(job => ({
          jobId: job.job_id,
          filename: job.filename
        }))
      );
    } finally {
      setIsUploading(false);
    }
  };

  return (
    <Button
      variant="contained"
      startIcon={isUploading ? <CircularProgress size={20} /> : <CloudUpload />}
      onClick={handleBatchUpload}
      disabled={!canUpload}
      color="primary"
    >
      {isUploading ? 'Uploading to Drive...' : `Upload All to Drive (${completedJobs.length})`}
    </Button>
  );
};
```

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Unit tests for Drive service and components (>90% coverage)
- [ ] Integration tests with Google Drive API
- [ ] E2E tests for Drive upload flow
- [ ] Error scenario testing completed
- [ ] Performance testing with multiple files
- [ ] Code review completed and approved
- [ ] Google Drive integration working end-to-end

## Dependencies
- **Requires:** Implementation Story 03 (Frontend Authentication)
- **Requires:** Implementation Story 09 (File Download System)
- **Integrates with:** Implementation Story 08 (Status Tracking)

## Test Scenarios

### Happy Path Tests
1. **Single File Upload**
   - User uploads converted file to Drive
   - Progress tracking works correctly
   - File appears in "Converted PDF Files" folder
   - Success notification displayed

2. **Batch Upload**
   - Multiple files uploaded simultaneously
   - Individual progress tracked
   - All files uploaded successfully
   - Folder organization maintained

3. **Folder Management**
   - Folder created automatically on first upload
   - Existing folder detected and used
   - Proper folder permissions set

### Error Scenarios
1. **Authentication Failures**
   - Expired OAuth token handled
   - Token refresh attempted
   - Clear error messages displayed
   - Re-authentication prompted if needed

2. **Network Errors**
   - Upload interrupted by network issues
   - Retry mechanism works correctly
   - Partial uploads handled gracefully

3. **Google API Limits**
   - Quota exceeded errors handled
   - Rate limiting respected
   - User informed of temporary restrictions

## Security Considerations
- [ ] OAuth token handled securely (no storage in localStorage)
- [ ] Drive API permissions limited to file scope
- [ ] User consent for Drive access clearly communicated
- [ ] File access restricted to user's own files
- [ ] API key and client ID properly configured

## Performance Considerations
- [ ] Efficient folder caching to reduce API calls
- [ ] Concurrent upload limits to respect API quotas
- [ ] Progress tracking without excessive updates
- [ ] Memory efficient file handling for large uploads

## Google Drive API Configuration
```typescript
// Configuration for Google Drive integration
const DRIVE_CONFIG = {
  apiKey: process.env.REACT_APP_GOOGLE_API_KEY,
  clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID,
  discoveryDocs: ['https://www.googleapis.com/discovery/v1/apis/drive/v3/rest'],
  scope: 'https://www.googleapis.com/auth/drive.file',
  folderName: 'Converted PDF Files',
  maxConcurrentUploads: 3,
  retryAttempts: 3,
  retryDelay: 1000
};
```

## Risks and Mitigation
- **Risk:** Google API quota limits affecting user experience
  - **Mitigation:** Rate limiting, queue management, clear user communication
- **Risk:** Large file uploads failing due to timeouts
  - **Mitigation:** Chunked uploads, progress tracking, retry mechanisms
- **Risk:** OAuth token expiration during long operations
  - **Mitigation:** Token refresh handling, graceful re-authentication

## Notes
- Consider implementing resumable uploads for large files
- Monitor Google Drive API usage and quotas
- Plan for future enhancements: custom folder selection, file organization
- Consider implementing Drive file sharing options