# Implementation Story 03: Google OAuth Authentication Frontend (Updated)

## Story Overview
**As a** user  
**I want** to authenticate using my Google account  
**So that** I can securely access the PDF conversion application and upload files to my Google Drive

## SMART Criteria

### Specific
Implement Google OAuth 2.0 authentication flow in the React frontend with proper session management, user state handling, and integration into the existing application shell.

### Measurable
- ✅ Google OAuth login functionality implemented
- ✅ User authentication state managed globally
- ✅ Protected routes implemented
- ✅ User profile component integrated into header
- ✅ Logout functionality working
- ✅ Token refresh handling implemented
- ✅ Authentication errors handled gracefully
- ✅ Existing application shell enhanced with auth features

### Achievable
Standard OAuth implementation using Google's official JavaScript SDK and React patterns, building on existing application shell.

### Relevant
Authentication is required for all PDF conversion features and Google Drive integration.

### Time-bound
**Estimated Duration:** 3 days  
**Sprint:** Sprint 1  
**Priority:** High (Required for all user-facing features)

## Technical Requirements

### Dependencies
- `gapi-script` or `@google-cloud/local-auth`
- `google-auth-library` (for token validation)
- React Context API for state management
- Axios interceptors for API authentication

### Integration Points
- Enhance existing AppShell component with user profile
- Replace authentication placeholder in header
- Add protected route wrapper to existing routing

## Acceptance Criteria

### AC1: OAuth Setup and Configuration
- [ ] Google OAuth client ID configured in environment variables
- [ ] Google API JavaScript library loaded and initialized
- [ ] OAuth scopes properly configured (drive.file, profile, email)
- [ ] Redirect URIs configured for all environments

### AC2: Login Flow Implementation
- [ ] Login page component created and integrated
- [ ] OAuth popup/redirect flow working correctly
- [ ] User consent screen shows correct permissions
- [ ] Successful authentication redirects to dashboard
- [ ] Failed authentication shows appropriate error message

### AC3: Authentication State Management
- [ ] AuthContext provides authentication state globally
- [ ] User information (name, email, picture) stored in context
- [ ] Authentication status persists across browser refreshes
- [ ] Token expiration handled automatically

### AC4: Application Shell Integration
- [ ] **NEW**: Replace header placeholder with UserProfile component
- [ ] **NEW**: Update AppShell to show authenticated vs unauthenticated states
- [ ] **NEW**: Integrate login/logout functionality into existing navigation
- [ ] **NEW**: Update dashboard to show personalized content when authenticated

### AC5: Protected Routes Enhancement
- [ ] **NEW**: Enhance existing routing with AuthGuard component
- [ ] **NEW**: Unauthenticated users see login page instead of dashboard
- [ ] **NEW**: Authenticated users can access all application areas
- [ ] **NEW**: Navigation updates based on authentication state

### AC6: User Interface Components
- [ ] Login button with Google branding guidelines
- [ ] **UPDATED**: UserProfile component integrated into existing header
- [ ] **UPDATED**: Logout functionality integrated into existing navigation
- [ ] Loading states during authentication process
- [ ] Error states for authentication failures

## Implementation Structure

### Enhanced AppShell Component
```typescript
// components/layout/AppShell.tsx (Updated)
import React from 'react';
import {
  Box,
  AppBar,
  Toolbar,
  Typography,
  Container
} from '@mui/material';
import { Outlet } from 'react-router-dom';
import { ErrorBoundary } from '../common/ErrorBoundary';
import { UserProfile } from './UserProfile';
import { LoginButton } from '../auth/LoginButton';
import { useAuth } from '../../context/AuthContext';

export const AppShell: React.FC = () => {
  const { isAuthenticated, isLoading } = useAuth();

  return (
    <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Enhanced Application Header */}
      <AppBar position="static" elevation={1}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            PDF OCR Converter
          </Typography>
          
          {/* Authentication-aware header content */}
          {isLoading ? (
            <Typography variant="body2" color="inherit">
              Loading...
            </Typography>
          ) : isAuthenticated ? (
            <UserProfile />
          ) : (
            <LoginButton />
          )}
        </Toolbar>
      </AppBar>

      {/* Main Content Area */}
      <Container maxWidth="xl" sx={{ flexGrow: 1, py: 3 }}>
        <ErrorBoundary>
          <Outlet />
        </ErrorBoundary>
      </Container>

      {/* Footer */}
      <Box 
        component="footer" 
        sx={{ 
          py: 2, 
          px: 3, 
          bgcolor: 'background.paper', 
          borderTop: 1, 
          borderColor: 'divider' 
        }}
      >
        <Typography variant="body2" color="text.secondary" align="center">
          © 2024 PDF OCR Converter. Convert your PDFs to searchable documents.
        </Typography>
      </Box>
    </Box>
  );
};
```

### Enhanced App Component with Authentication
```typescript
// App.tsx (Updated)
import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from '@mui/material/styles';
import { CssBaseline } from '@mui/material';
import { theme } from './styles/theme';
import { AuthProvider } from './context/AuthContext';
import { AppShell } from './components/layout/AppShell';
import { Dashboard } from './pages/Dashboard';
import { LoginPage } from './pages/LoginPage';
import { AuthGuard } from './components/auth/AuthGuard';
import { NotFound } from './pages/NotFound';

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <Router>
          <Routes>
            <Route path="/login" element={<LoginPage />} />
            <Route path="/" element={<AppShell />}>
              <Route index element={
                <AuthGuard>
                  <Dashboard />
                </AuthGuard>
              } />
              <Route path="*" element={<NotFound />} />
            </Route>
          </Routes>
        </Router>
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;
```

### Enhanced Dashboard with Authentication
```typescript
// pages/Dashboard.tsx (Updated)
import React from 'react';
import {
  Box,
  Typography,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
  Alert
} from '@mui/material';
import { useAuth } from '../context/AuthContext';

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
          You're successfully authenticated and ready to convert PDFs.
        </Typography>
      </Alert>

      <Typography variant="h4" gutterBottom>
        PDF OCR Converter Dashboard
      </Typography>
      
      <Typography variant="body1" color="text.secondary" paragraph>
        Convert your PDF files into searchable documents using OCR technology.
      </Typography>

      {/* Existing placeholder cards remain the same but now show as "ready for implementation" */}
      <Grid container spacing={3}>
        {/* Upload Section - Ready for Story 05 */}
        <Grid item xs={12} md={6}>
          <Card sx={{ height: '100%' }}>
            <CardContent>
              {/* ... existing upload placeholder content ... */}
              <Typography variant="caption" color="success.main">
                ✅ Authentication complete - Ready for file upload implementation
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Other placeholder cards with similar "ready" indicators */}
        {/* ... */}
      </Grid>
    </Box>
  );
};
```

## Integration Changes from Story 01.1

### Removed from Original Story 11:
- ✅ Basic application shell (now in Story 01.1)
- ✅ Basic header structure (now in Story 01.1)
- ✅ Basic routing setup (now in Story 01.1)
- ✅ Error boundary implementation (now in Story 01.1)
- ✅ Theme configuration (now in Story 01.1)

### Enhanced in This Story:
- ✅ Authentication-aware header
- ✅ User profile integration
- ✅ Protected routing
- ✅ Personalized dashboard content
- ✅ Login/logout flow integration

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Authentication integrates seamlessly with existing application shell
- [ ] User can log in and see personalized dashboard
- [ ] Protected routes prevent unauthorized access
- [ ] Existing application structure is enhanced, not replaced
- [ ] All placeholder components show "ready for implementation" status
- [ ] Code review completed and approved

## Dependencies
- **Requires:** Implementation Story 01 (Frontend Bootstrap)
- **Requires:** Implementation Story 01.1 (Basic Application Shell)
- **Requires:** Implementation Story 02 (Backend Bootstrap)
- **Requires:** Implementation Story 04 (Backend Authentication)
- **Prepares for:** All subsequent user-facing features

## Notes
- This story enhances the existing application shell rather than replacing it
- Authentication state is now available throughout the application
- Placeholder components can now show authenticated vs unauthenticated states
- The application remains fully functional and demonstrable at each step