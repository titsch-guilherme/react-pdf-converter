# Implementation Story 05: PDF File Upload and Validation (Updated)

## Story Overview
**As a** user  
**I want** to upload multiple PDF files through a drag-and-drop interface  
**So that** I can prepare them for OCR conversion with proper validation and feedback

## SMART Criteria

### Specific
Implement a file upload interface with drag-and-drop functionality, file validation, and batch upload capabilities for PDF files, integrating into the existing dashboard layout.

### Measurable
- ✅ Drag-and-drop zone implemented with visual feedback
- ✅ File browser upload option available
- ✅ Multiple file selection supported
- ✅ PDF file type validation implemented
- ✅ File size validation (configurable limit)
- ✅ File list display with remove/edit options
- ✅ Upload progress indication
- ✅ Error handling for invalid files
- ✅ **NEW**: Integration with existing dashboard layout
- ✅ **NEW**: Replace upload placeholder in dashboard

### Achievable
Standard file upload implementation using React Dropzone and HTML5 file APIs, building on existing application structure.

### Relevant
Essential for users to submit PDF files for OCR conversion processing.

### Time-bound
**Estimated Duration:** 3 days  
**Sprint:** Sprint 2  
**Priority:** High (Core user functionality)

## Technical Requirements

### Dependencies
- `react-dropzone` ^14.x for drag-and-drop functionality
- `@mui/material` components for UI
- File validation utilities
- Progress tracking hooks

### Integration Points
- Replace upload placeholder card in existing Dashboard component
- Integrate with existing authentication context
- Prepare for status tracking integration (Story 08)

## Acceptance Criteria

### AC1: Dashboard Integration
- [ ] **NEW**: Replace upload placeholder card in Dashboard component
- [ ] **NEW**: File upload area integrated into existing grid layout
- [ ] **NEW**: Upload component respects existing responsive design
- [ ] **NEW**: Upload area shows authentication-aware content
- [ ] **NEW**: Seamless integration with existing Material-UI theme

### AC2: Drag-and-Drop Interface
- [ ] Drag-and-drop zone with clear visual boundaries
- [ ] Visual feedback during drag operations (hover states)
- [ ] Drop zone highlights when files are dragged over
- [ ] Multiple files can be dropped simultaneously
- [ ] Keyboard accessibility for file selection

### AC3: File Browser Integration
- [ ] "Browse Files" button opens file selection dialog
- [ ] Multiple file selection enabled in file dialog
- [ ] File dialog filters to PDF files only
- [ ] Selected files added to upload queue

### AC4: File Validation
- [ ] PDF file type validation (MIME type and extension)
- [ ] File size validation with configurable limits
- [ ] Basic PDF structure validation (file headers)
- [ ] Duplicate file detection and handling
- [ ] Invalid files rejected with clear error messages

### AC5: File List Management
- [ ] Selected files displayed in a list/table format
- [ ] File information shown (name, size, type)
- [ ] Individual file removal option
- [ ] Clear all files option
- [ ] File reordering capability (optional)

### AC6: Upload Progress and Feedback
- [ ] Upload progress indicator for each file
- [ ] Overall batch upload progress
- [ ] Success/error states for each file
- [ ] Retry option for failed uploads
- [ ] Cancel upload functionality

### AC7: User Experience Enhancement
- [ ] **NEW**: Upload area shows user's name and personalized content
- [ ] **NEW**: Integration with existing loading states
- [ ] **NEW**: Consistent error handling with application error boundary
- [ ] **NEW**: Upload success integrates with existing notification system
- [ ] **NEW**: Prepare upload area for status tracking integration

## Implementation Structure

### Enhanced Dashboard Component
```typescript
// pages/Dashboard.tsx (Updated for File Upload Integration)
import React from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Alert
} from '@mui/material';
import { useAuth } from '../context/AuthContext';
import { FileUploadSection } from '../components/upload/FileUploadSection';
import { StatusPlaceholder } from '../components/placeholders/StatusPlaceholder';
import { DownloadPlaceholder } from '../components/placeholders/DownloadPlaceholder';
import { DrivePlaceholder } from '../components/placeholders/DrivePlaceholder';

export const Dashboard: React.FC = () => {
  const { user } = useAuth();

  return (
    <Box>
      {/* Personalized welcome message */}
      <Alert severity="success" sx={{ mb: 3 }}>
        <Typography variant="h6">
          Welcome back, {user?.name}! 👋
        </Typography>
        <Typography variant="body2">
          Upload your PDF files below to get started with OCR conversion.
        </Typography>
      </Alert>

      <Typography variant="h4" gutterBottom>
        PDF OCR Converter Dashboard
      </Typography>

      <Grid container spacing={3}>
        {/* File Upload Section - Now Implemented */}
        <Grid item xs={12} md={6}>
          <FileUploadSection />
        </Grid>

        {/* Status Section - Still Placeholder, Ready for Story 08 */}
        <Grid item xs={12} md={6}>
          <StatusPlaceholder />
        </Grid>

        {/* Download Section - Placeholder, Ready for Story 09 */}
        <Grid item xs={12} md={6}>
          <DownloadPlaceholder />
        </Grid>

        {/* Google Drive Section - Placeholder, Ready for Story 10 */}
        <Grid item xs={12} md={6}>
          <DrivePlaceholder />
        </Grid>
      </Grid>
    </Box>
  );
};
```

### File Upload Section Component
```typescript
// components/upload/FileUploadSection.tsx
import React, { useState } from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Alert
} from '@mui/material';
import { CloudUpload } from '@mui/icons-material';
import { FileUploader } from './FileUploader';
import { FileList } from './FileList';
import { UploadProgress } from './UploadProgress';
import { useAuth } from '../../context/AuthContext';

interface FileWithStatus {
  file: File;
  id: string;
  status: 'pending' | 'uploading' | 'success' | 'error';
  progress: number;
  error?: string;
}

export const FileUploadSection: React.FC = () => {
  const { user } = useAuth();
  const [files, setFiles] = useState<FileWithStatus[]>([]);
  const [isUploading, setIsUploading] = useState(false);

  const handleFilesSelected = (newFiles: File[]) => {
    const filesWithStatus: FileWithStatus[] = newFiles.map(file => ({
      file,
      id: `${file.name}-${Date.now()}`,
      status: 'pending',
      progress: 0
    }));
    
    setFiles(prev => [...prev, ...filesWithStatus]);
  };

  const handleRemoveFile = (id: string) => {
    setFiles(prev => prev.filter(f => f.id !== id));
  };

  const handleStartUpload = async () => {
    setIsUploading(true);
    // Upload logic will be implemented when backend is ready (Story 06)
    // For now, simulate upload process
    
    for (const fileItem of files) {
      if (fileItem.status === 'pending') {
        // Simulate upload progress
        setFiles(prev => prev.map(f => 
          f.id === fileItem.id 
            ? { ...f, status: 'uploading' as const }
            : f
        ));
        
        // Simulate progress updates
        for (let progress = 0; progress <= 100; progress += 20) {
          await new Promise(resolve => setTimeout(resolve, 200));
          setFiles(prev => prev.map(f => 
            f.id === fileItem.id 
              ? { ...f, progress }
              : f
          ));
        }
        
        // Mark as complete
        setFiles(prev => prev.map(f => 
          f.id === fileItem.id 
            ? { ...f, status: 'success' as const, progress: 100 }
            : f
        ));
      }
    }
    
    setIsUploading(false);
  };

  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <CloudUpload sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h6">
            Upload PDF Files
          </Typography>
        </Box>
        
        <Typography variant="body2" color="text.secondary" paragraph>
          Hi {user?.name}! Upload your PDF files to convert them into searchable documents.
        </Typography>

        {files.length === 0 ? (
          <FileUploader 
            onFilesSelected={handleFilesSelected}
            disabled={isUploading}
          />
        ) : (
          <>
            <FileList 
              files={files}
              onRemoveFile={handleRemoveFile}
              onStartUpload={handleStartUpload}
              isUploading={isUploading}
            />
            
            {isUploading && (
              <Box sx={{ mt: 2 }}>
                <UploadProgress files={files} />
              </Box>
            )}
          </>
        )}

        {files.some(f => f.status === 'success') && (
          <Alert severity="info" sx={{ mt: 2 }}>
            <Typography variant="body2">
              Files uploaded successfully! Status tracking will be available in the next update.
            </Typography>
          </Alert>
        )}
      </CardContent>
    </Card>
  );
};
```

### Updated Placeholder Components
```typescript
// components/placeholders/StatusPlaceholder.tsx
import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Button,
  Chip
} from '@mui/material';
import { Assessment } from '@mui/icons-material';

export const StatusPlaceholder: React.FC = () => {
  return (
    <Card sx={{ height: '100%' }}>
      <CardContent>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
          <Assessment sx={{ mr: 1, color: 'primary.main' }} />
          <Typography variant="h6">
            Conversion Status
          </Typography>
          <Chip 
            label="Next: Story 08" 
            size="small" 
            color="info" 
            sx={{ ml: 'auto' }}
          />
        </Box>
        <Typography variant="body2" color="text.secondary" paragraph>
          Track the progress of your PDF conversions with real-time updates.
        </Typography>
        <Typography variant="caption" color="success.main" display="block" sx={{ mb: 2 }}>
          ✅ Authentication complete
          <br />
          ✅ File upload ready
          <br />
          🔄 Status tracking coming next
        </Typography>
        <Button variant="outlined" disabled>
          View Status (Story 08)
        </Button>
      </CardContent>
    </Card>
  );
};
```

## Integration Changes from Original Story

### Enhanced Integration:
- ✅ **NEW**: Seamless integration with existing Dashboard layout
- ✅ **NEW**: Respects existing authentication context
- ✅ **NEW**: Uses established Material-UI theme and patterns
- ✅ **NEW**: Integrates with existing error handling
- ✅ **NEW**: Prepares for status tracking integration

### Removed Complexity:
- ✅ No need to create new layout structure
- ✅ No need to establish new routing
- ✅ No need to create new theme or styling patterns
- ✅ Builds on existing responsive framework

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] File upload replaces placeholder in existing dashboard
- [ ] Upload functionality works within existing application structure
- [ ] Integration respects existing authentication and theming
- [ ] Placeholder components updated to show implementation progress
- [ ] Ready for backend integration (Story 06)
- [ ] Code review completed and approved

## Dependencies
- **Requires:** Implementation Story 01 (Frontend Bootstrap)
- **Requires:** Implementation Story 01.1 (Basic Application Shell)
- **Requires:** Implementation Story 03 (Frontend Authentication)
- **Prepares for:** Implementation Story 06 (Backend File Processing)
- **Integrates with:** Implementation Story 08 (Status Tracking)

## Integration Points for Future Stories

### For Story 06 (Backend Integration):
- Replace simulated upload with actual API calls
- Add proper error handling for backend failures
- Implement actual file validation with backend

### For Story 08 (Status Tracking):
- Connect uploaded files to status tracking system
- Replace success alert with status panel integration
- Add real-time status updates

## Notes
- This story enhances the existing dashboard rather than creating new layouts
- Upload functionality is immediately visible and usable
- Placeholder components show clear progression of implementation
- The application remains fully functional and demonstrable
- Ready for seamless backend integration in Story 06