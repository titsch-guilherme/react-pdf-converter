# React Code Guidelines

## 1. Project Structure
- Organize by feature or domain (recommended for scalability)
- For batch functionality, components and hooks for job lists and file-tracking should be grouped logically
- Core folders: `/src/components`, `/src/pages`, `/src/api`, `/src/styles`, `/src/hooks`, `/src/context`, `/src/utils`, `/src/tests`, `/src/assets`, `/public`
    - `/components`: Reusable UI elements organized by feature
    - `/pages`: Route-level components
    - `/api`: API abstraction layer (Axios wrappers with session management)
    - `/hooks`: Custom React hooks for state management and API interactions
    - `/context`: Context providers for global state (auth, jobs, sessions)
    - `/styles`: CSS-in-JS/themes or global styles
    - `/utils`: Shared helpers and utilities
    - `/assets`: Images, fonts, icons
    - `/tests`: Unit, integration, and E2E tests
    - `/public`: Static files, index.html
    - `App.tsx`/`App.jsx`, `index.tsx`/`index.jsx`: Entry points

Example structure:
```
frontend/
├── src/
│   ├── components/
│   │   ├── auth/
│   │   │   ├── LoginButton.tsx
│   │   │   └── AuthGuard.tsx
│   │   ├── upload/
│   │   │   ├── FileUploader.tsx
│   │   │   ├── DropZone.tsx
│   │   │   └── FileList.tsx
│   │   ├── status/
│   │   │   ├── StatusPanel.tsx
│   │   │   ├── FileStatusRow.tsx
│   │   │   └── BatchActions.tsx
│   │   └── common/
│   │       ├── LoadingSpinner.tsx
│   │       └── ErrorBoundary.tsx
│   ├── pages/
│   │   ├── LoginPage.tsx
│   │   └── ConversionPage.tsx
│   ├── hooks/
│   │   ├── useAuth.ts
│   │   ├── useBatchStatus.ts
│   │   ├── useFileUpload.ts
│   │   └── useGoogleDrive.ts
│   ├── context/
│   │   ├── AuthContext.tsx
│   │   └── JobsContext.tsx
│   ├── api/
│   │   ├── auth.ts
│   │   ├── conversion.ts
│   │   ├── status.ts
│   │   └── client.ts
│   ├── utils/
│   │   ├── fileValidation.ts
│   │   ├── errorHandling.ts
│   │   └── constants.ts
│   └── tests/
│       ├── components/
│       ├── hooks/
│       ├── api/
│       └── utils/
```

## 2. State Management

### Global State Strategy
- Use React Context API for app-global state (auth, user/session, drive info)
- Consider Redux/RTK only if app complexity significantly increases
- Avoid unnecessary global state; document purpose of any context provider

### Job and Session Management
```typescript
// Example AuthContext structure
interface AuthContextType {
  user: User | null;
  sessionId: string | null;
  isAuthenticated: boolean;
  login: (googleToken: string) => Promise<void>;
  logout: () => void;
  refreshSession: () => Promise<void>;
}

// Example JobsContext structure
interface JobsContextType {
  jobs: Job[];
  addJobs: (newJobs: Job[]) => void;
  updateJob: (jobId: string, updates: Partial<Job>) => void;
  removeJob: (jobId: string) => void;
  clearCompletedJobs: () => void;
}
```

### Local State Management
- Prefer local state/hooks for UI-local logic
- Track upload status and progress for each file individually (array/object of file jobs)
- Store jobs in Context/global state for batch/parallel flows
- Use hooks (e.g., useReducer) for complex job status updates
- All relevant state changes should trigger component re-renders and UI updates
- Handle async batch polling/status updating with proper interval clearing and cleanup

## 3. Component Design & UI/UX

### Component Architecture
- Prioritize small, reusable, single-purpose components
- Function components and hooks (no class components)
- Use Material-UI (MUI) for styling/themes and consistent design system
- Always handle async UI states (loading, errors, empty states)
- Fully accessible (a11y): ARIA labels, keyboard navigation, proper contrast

### Batch-Aware UI Components
```typescript
// Example batch-aware component structure
interface FileStatusRowProps {
  job: Job;
  onDownload: (jobId: string) => void;
  onUploadToDrive: (jobId: string) => void;
  onRetry: (jobId: string) => void;
}

const FileStatusRow: React.FC<FileStatusRowProps> = ({ 
  job, 
  onDownload, 
  onUploadToDrive, 
  onRetry 
}) => {
  return (
    <TableRow>
      <TableCell>{job.filename}</TableCell>
      <TableCell>
        <StatusChip status={job.status} />
      </TableCell>
      <TableCell>
        {job.status === 'processing' && (
          <LinearProgress variant="determinate" value={job.progress} />
        )}
      </TableCell>
      <TableCell>
        <BatchActionButtons 
          job={job}
          onDownload={onDownload}
          onUploadToDrive={onUploadToDrive}
          onRetry={onRetry}
        />
      </TableCell>
    </TableRow>
  );
};
```

### Responsive Design Requirements
- Responsive design: mobile, tablet, desktop
- Design batch-aware components that handle lists: map over job arrays for UI
- Show clear status, errors, download/upload per file
- Batch actions (upload all to Drive, download all) enabled when applicable
- Live feedback for each file (progress bars, error states, success icons)
- Accessible, responsive, and clear split-pane layout

## 4. Networking & API Integration

### API Client Structure
```typescript
// Example API client with session management
import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';

class ApiClient {
  private client: AxiosInstance;
  private sessionId: string | null = null;

  constructor(baseURL: string) {
    this.client = axios.create({ baseURL });
    this.setupInterceptors();
  }

  private setupInterceptors() {
    // Request interceptor to add session ID
    this.client.interceptors.request.use((config) => {
      if (this.sessionId) {
        config.headers['session-id'] = this.sessionId;
      }
      return config;
    });

    // Response interceptor for error handling
    this.client.interceptors.response.use(
      (response) => response,
      (error) => {
        if (error.response?.status === 401) {
          // Handle session expiry
          this.handleAuthError();
        }
        return Promise.reject(error);
      }
    );
  }

  setSessionId(sessionId: string) {
    this.sessionId = sessionId;
  }

  async validateToken(googleToken: string) {
    const response = await this.client.post('/api/v1/auth/validate', {
      access_token: googleToken
    });
    this.setSessionId(response.data.session_id);
    return response.data;
  }

  async uploadFiles(files: File[]) {
    const formData = new FormData();
    files.forEach(file => formData.append('files', file));
    
    return this.client.post('/api/v1/convert', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  }

  async getJobStatus(jobId?: string) {
    const endpoint = jobId ? `/api/v1/status/${jobId}` : '/api/v1/status';
    return this.client.get(endpoint);
  }
}
```

### Batch Processing Hooks
```typescript
// Example custom hook for batch status management
import { useState, useEffect, useCallback } from 'react';

interface UseBatchStatusOptions {
  pollingInterval?: number;
  autoStart?: boolean;
}

export const useBatchStatus = (options: UseBatchStatusOptions = {}) => {
  const { pollingInterval = 3000, autoStart = true } = options;
  const [jobs, setJobs] = useState<Job[]>([]);
  const [isPolling, setIsPolling] = useState(autoStart);
  const [error, setError] = useState<string | null>(null);

  const updateJobsStatus = useCallback(async () => {
    try {
      const response = await apiClient.getJobStatus();
      setJobs(response.data.jobs);
      setError(null);
    } catch (err) {
      setError('Failed to fetch job status');
      console.error('Status polling error:', err);
    }
  }, []);

  useEffect(() => {
    let intervalId: NodeJS.Timeout;

    if (isPolling && jobs.some(job => 
      job.status === 'pending' || job.status === 'processing'
    )) {
      intervalId = setInterval(updateJobsStatus, pollingInterval);
    }

    return () => {
      if (intervalId) clearInterval(intervalId);
    };
  }, [isPolling, jobs, updateJobsStatus, pollingInterval]);

  const startPolling = useCallback(() => setIsPolling(true), []);
  const stopPolling = useCallback(() => setIsPolling(false), []);

  return {
    jobs,
    setJobs,
    isPolling,
    startPolling,
    stopPolling,
    error,
    refreshStatus: updateJobsStatus
  };
};
```

### Error Handling Strategy
- Encapsulate all API calls in `/api` folder/modules
- Axios interceptors for auth errors (token/session expiry)
- Display clear errors/tips for network failures
- Validate user input; handle server-side errors gracefully
- Batch upload logic (multi-file form POSTs), per-job status endpoint polling
- Encapsulate job list logic in API modules/hooks
- Handle concurrent network requests and merging of responses in state

## 5. Code Quality & Type Safety

### TypeScript Implementation
```typescript
// Example type definitions
interface Job {
  job_id: string;
  filename: string;
  status: 'pending' | 'processing' | 'done' | 'failed';
  progress: number;
  error: string | null;
  download_url: string | null;
  created_at: string;
}

interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
}

interface ApiError {
  error: string;
  error_code: string;
  details?: Record<string, any>;
}

// Example component with proper typing
interface FileUploaderProps {
  onFilesSelected: (files: File[]) => void;
  maxFiles?: number;
  maxFileSize?: number;
  acceptedTypes?: string[];
  disabled?: boolean;
}

const FileUploader: React.FC<FileUploaderProps> = ({
  onFilesSelected,
  maxFiles = 10,
  maxFileSize = 50 * 1024 * 1024, // 50MB
  acceptedTypes = ['application/pdf'],
  disabled = false
}) => {
  // Component implementation
};
```

### Code Standards
- TypeScript preferred for all new code
- Enforce linting (ESLint) and consistent styles (Prettier)
- Use PropTypes for JS-only projects where TypeScript is not used
- Write descriptive JSDoc/TSdoc comments for complex functions/components
- Maintain strong type safety (with TypeScript) over job/file states
- Test UI for batch flows, including rapid uploads, job failures, and edge-cases

## 6. Automated Testing Strategy

### Testing Structure
- Use Jest & React Testing Library for unit/integration/component tests
- Cypress for E2E tests (login, file upload, user flows)
- Mock network/API calls, Google APIs in tests
- Test coverage tools (Jest `--coverage`, target >=90%)
- Place tests in relevant `/src/tests`, alongside components, or mirrored structure

### Testing Examples
```typescript
// Example component test
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { FileUploader } from '../components/upload/FileUploader';

describe('FileUploader', () => {
  it('handles multiple file selection', async () => {
    const mockOnFilesSelected = jest.fn();
    render(<FileUploader onFilesSelected={mockOnFilesSelected} />);

    const input = screen.getByLabelText(/upload files/i);
    const files = [
      new File(['content1'], 'test1.pdf', { type: 'application/pdf' }),
      new File(['content2'], 'test2.pdf', { type: 'application/pdf' })
    ];

    fireEvent.change(input, { target: { files } });

    await waitFor(() => {
      expect(mockOnFilesSelected).toHaveBeenCalledWith(files);
    });
  });

  it('validates file types and shows errors', async () => {
    const mockOnFilesSelected = jest.fn();
    render(<FileUploader onFilesSelected={mockOnFilesSelected} />);

    const input = screen.getByLabelText(/upload files/i);
    const invalidFile = new File(['content'], 'test.txt', { type: 'text/plain' });

    fireEvent.change(input, { target: { files: [invalidFile] } });

    await waitFor(() => {
      expect(screen.getByText(/invalid file type/i)).toBeInTheDocument();
      expect(mockOnFilesSelected).not.toHaveBeenCalled();
    });
  });
});

// Example hook test
import { renderHook, act } from '@testing-library/react';
import { useBatchStatus } from '../hooks/useBatchStatus';

jest.mock('../api/client');

describe('useBatchStatus', () => {
  it('polls for status updates when jobs are processing', async () => {
    const mockGetJobStatus = jest.fn().mockResolvedValue({
      data: { jobs: [{ job_id: '1', status: 'processing', progress: 50 }] }
    });

    const { result } = renderHook(() => useBatchStatus({ pollingInterval: 100 }));

    act(() => {
      result.current.setJobs([{ job_id: '1', status: 'processing', progress: 0 }]);
    });

    await waitFor(() => {
      expect(mockGetJobStatus).toHaveBeenCalled();
    }, { timeout: 200 });
  });
});
```

### E2E Testing Requirements
- Automate tests in CI (GitHub Actions, etc.) for all commits/PRs
- Unit tests for per-file and batch flows with Jest/React Testing Library
- Test complex state updates and error propagation
- E2E tests for UI, batch uploads and status handling
- Test scenarios:
  - Complete user flow from login to file conversion
  - Batch file upload and status tracking
  - Error handling and recovery
  - Google Drive integration
  - Session management and token refresh

## 7. Security & Maintainability

### Security Best Practices
- Never commit API keys or secrets to source code
- Use HTTPS for all API and OAuth callbacks
- Regularly update npm dependencies (audit with npm/yarn, Dependabot)
- Use Docker for consistent development and production environments
- Batch file validation on the client before upload
- Never expose sensitive metadata; all uploads must be scoped/authenticated
- Implement proper session management with automatic token refresh

### Google Drive Integration Security
```typescript
// Example secure Google Drive integration
class GoogleDriveService {
  private gapi: any;
  private accessToken: string;

  async initializeGapi() {
    await new Promise((resolve) => {
      gapi.load('auth2:client', resolve);
    });

    await gapi.client.init({
      clientId: process.env.REACT_APP_GOOGLE_CLIENT_ID,
      scope: 'https://www.googleapis.com/auth/drive.file'
    });
  }

  async signIn(): Promise<string> {
    const authInstance = gapi.auth2.getAuthInstance();
    const user = await authInstance.signIn();
    this.accessToken = user.getAuthResponse().access_token;
    return this.accessToken;
  }

  async uploadFile(file: Blob, filename: string): Promise<string> {
    // Ensure folder exists
    const folderId = await this.ensureConvertedFilesFolder();
    
    // Upload file with proper error handling
    const metadata = {
      name: filename,
      parents: [folderId]
    };

    const form = new FormData();
    form.append('metadata', new Blob([JSON.stringify(metadata)], {
      type: 'application/json'
    }));
    form.append('file', file);

    const response = await fetch(
      'https://www.googleapis.com/upload/drive/v3/files?uploadType=multipart',
      {
        method: 'POST',
        headers: {
          'Authorization': `Bearer ${this.accessToken}`
        },
        body: form
      }
    );

    if (!response.ok) {
      throw new Error(`Drive upload failed: ${response.statusText}`);
    }

    const result = await response.json();
    return result.id;
  }
}
```

## 8. Performance Optimization

### Component Optimization
- Use React.memo for expensive components
- Implement proper dependency arrays in useEffect and useCallback
- Avoid unnecessary re-renders with proper state structure
- Use virtualization for large job lists
- Implement proper loading states and skeleton screens

### File Handling Optimization
```typescript
// Example optimized file handling
const useFileUpload = () => {
  const [uploadProgress, setUploadProgress] = useState<Record<string, number>>({});

  const uploadFiles = useCallback(async (files: File[]) => {
    // Validate files before upload
    const validFiles = files.filter(file => 
      file.type === 'application/pdf' && file.size <= MAX_FILE_SIZE
    );

    if (validFiles.length !== files.length) {
      // Handle validation errors
      showError('Some files were rejected due to validation errors');
    }

    // Upload files with progress tracking
    const uploadPromises = validFiles.map(async (file, index) => {
      const formData = new FormData();
      formData.append('files', file);

      return apiClient.uploadFiles([file], {
        onUploadProgress: (progressEvent) => {
          const progress = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(prev => ({
            ...prev,
            [file.name]: progress
          }));
        }
      });
    });

    try {
      const results = await Promise.allSettled(uploadPromises);
      // Handle mixed success/failure results
      return results;
    } catch (error) {
      console.error('Batch upload error:', error);
      throw error;
    }
  }, []);

  return { uploadFiles, uploadProgress };
};
```

## 9. Documentation Requirements

### Code Documentation
- Document folder structure, core patterns, testing process in README
- Add in-code comments where business logic or integration is non-trivial
- Code and README should explain batch-capable layouts, job-tracking logic, and how to extend batch functionality
- Component documentation with Storybook (optional but recommended)

### README Structure
```markdown
# PDF OCR Converter Frontend

## Features
- Batch PDF file upload and conversion
- Real-time status tracking
- Google Drive integration
- Responsive design with accessibility support

## Getting Started
### Prerequisites
- Node.js 20.x LTS
- npm or yarn

### Installation
1. Clone the repository
2. Install dependencies: `npm install`
3. Set up environment variables (see .env.example)
4. Start development server: `npm start`

### Environment Variables
- REACT_APP_API_BASE_URL: Backend API URL
- REACT_APP_GOOGLE_CLIENT_ID: Google OAuth client ID

## Architecture
### State Management
- React Context for global state (auth, jobs)
- Local state for UI-specific logic
- Custom hooks for API interactions

### Component Structure
- Feature-based organization
- Reusable components in /components
- Page-level components in /pages

## Testing
- Unit tests: `npm test`
- E2E tests: `npm run cypress`
- Coverage report: `npm run test:coverage`

## Deployment
- Build: `npm run build`
- Docker: `docker build -t pdf-converter-frontend .`
```

## 10. Development Workflow

### Git Workflow
- Feature branches for all development
- Pull request reviews required
- Automated testing in CI/CD
- Semantic versioning for releases

### Development Tools
- ESLint and Prettier for code quality
- Husky for pre-commit hooks
- Conventional commits for changelog generation
- Dependabot for dependency updates

### Debugging and Development
- React Developer Tools for component debugging
- Redux DevTools (if using Redux)
- Network tab for API debugging
- Console logging with proper log levels
- Error boundaries for graceful error handling