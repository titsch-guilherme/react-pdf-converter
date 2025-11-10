# Implementation Story 01: Frontend Application Bootstrap - Task Breakdown

## Overview
This document breaks down Implementation Story 01 into specific, actionable tasks that can be completed sequentially. Each task includes clear deliverables, acceptance criteria, and estimated time.

**Total Estimated Time:** 2 days (16 hours)  
**Prerequisites:** Node.js 20.x LTS, Git, Docker Desktop

---

## Phase 1: Project Initialization (4 hours)

### Task 1.1: Environment Setup and Project Creation
**Estimated Time:** 1.5 hours  
**Priority:** Critical

#### Deliverables:
- [ ] New React project created with Vite
- [ ] Initial project structure established
- [ ] Git repository initialized with proper .gitignore

#### Steps:
1. **Create Vite React Project:**
   ```bash
   npm create vite@latest frontend -- --template react-ts
   cd frontend
   npm install
   ```

2. **Verify Initial Setup:**
   ```bash
   npm run dev
   # Should open http://localhost:5173 with Vite + React page
   ```

3. **Initialize Git Repository:**
   ```bash
   git init
   git add .
   git commit -m "Initial Vite + React + TypeScript setup"
   ```

4. **Create Project Structure:**
   ```bash
   mkdir -p src/{components/{common,auth,upload,status},pages,hooks,context,api,utils,styles,tests,assets}
   touch src/components/index.ts src/pages/index.ts src/hooks/index.ts
   ```

#### Acceptance Criteria:
- [ ] `npm run dev` starts development server successfully
- [ ] Application loads at http://localhost:5173
- [ ] All required directories are created
- [ ] Git repository is initialized with clean commit history

---

### Task 1.2: TypeScript Configuration and Path Aliases
**Estimated Time:** 1 hour  
**Priority:** High

#### Deliverables:
- [ ] Enhanced TypeScript configuration with strict mode
- [ ] Path aliases configured for absolute imports
- [ ] TypeScript compilation working without errors

#### Steps:
1. **Update tsconfig.json:**
   ```json
   {
     "compilerOptions": {
       "target": "ES2020",
       "useDefineForClassFields": true,
       "lib": ["ES2020", "DOM", "DOM.Iterable"],
       "module": "ESNext",
       "skipLibCheck": true,
       "moduleResolution": "bundler",
       "allowImportingTsExtensions": true,
       "resolveJsonModule": true,
       "isolatedModules": true,
       "noEmit": true,
       "jsx": "react-jsx",
       "strict": true,
       "noUnusedLocals": true,
       "noUnusedParameters": true,
       "noFallthroughCasesInSwitch": true,
       "baseUrl": ".",
       "paths": {
         "@/*": ["src/*"],
         "@/components/*": ["src/components/*"],
         "@/pages/*": ["src/pages/*"],
         "@/hooks/*": ["src/hooks/*"],
         "@/utils/*": ["src/utils/*"],
         "@/api/*": ["src/api/*"],
         "@/context/*": ["src/context/*"],
         "@/styles/*": ["src/styles/*"]
       }
     },
     "include": ["src"],
     "references": [{ "path": "./tsconfig.node.json" }]
   }
   ```

2. **Update vite.config.ts:**
   ```typescript
   import { defineConfig } from 'vite'
   import react from '@vitejs/plugin-react'
   import path from 'path'

   export default defineConfig({
     plugins: [react()],
     resolve: {
       alias: {
         '@': path.resolve(__dirname, './src'),
         '@/components': path.resolve(__dirname, './src/components'),
         '@/pages': path.resolve(__dirname, './src/pages'),
         '@/hooks': path.resolve(__dirname, './src/hooks'),
         '@/utils': path.resolve(__dirname, './src/utils'),
         '@/api': path.resolve(__dirname, './src/api'),
         '@/context': path.resolve(__dirname, './src/context'),
         '@/styles': path.resolve(__dirname, './src/styles'),
       },
     },
     server: {
       port: 3000,
       open: true,
     },
     build: {
       outDir: 'build',
       sourcemap: true,
     },
   })
   ```

3. **Test Path Aliases:**
   - Create a test component using absolute imports
   - Verify TypeScript compilation works

#### Acceptance Criteria:
- [ ] TypeScript strict mode is enabled
- [ ] Path aliases work for imports (e.g., `import { Component } from '@/components/Component'`)
- [ ] No TypeScript compilation errors
- [ ] Development server runs on port 3000

---

### Task 1.3: Core Dependencies Installation
**Estimated Time:** 1.5 hours  
**Priority:** Critical

#### Deliverables:
- [ ] All core dependencies installed with correct versions
- [ ] Package.json updated with proper scripts
- [ ] Dependencies verified to work together

#### Steps:
1. **Install Core Dependencies:**
   ```bash
   npm install react@^19.2.0 react-dom@^19.2.0
   npm install @mui/material@^7.3.5 @mui/icons-material@^7.3.5
   npm install @emotion/react@^11.14.0 @emotion/styled@^11.14.1
   npm install react-router-dom@^7.9.5
   npm install axios@^1.13.2
   npm install react-dropzone@^14.3.8
   npm install react-toastify@^11.0.5
   npm install web-vitals@^5.1.0
   ```

2. **Install Development Dependencies:**
   ```bash
   npm install -D @types/react@^19.2.2 @types/react-dom@^19.2.2
   npm install -D @types/node@^24.10.0 @types/jest@^30.0.0
   npm install -D @testing-library/react@^16.3.0
   npm install -D @testing-library/jest-dom@^6.9.1
   npm install -D @testing-library/user-event@^14.5.2
   npm install -D jest@^30.2.0 jest-environment-jsdom@^30.2.0
   npm install -D eslint@^9.39.1 prettier@^3.6.2
   npm install -D @typescript-eslint/eslint-plugin@^8.21.0
   npm install -D @typescript-eslint/parser@^8.21.0
   npm install -D eslint-plugin-react@^7.37.2
   npm install -D eslint-plugin-react-hooks@^5.1.0
   npm install -D husky@^9.1.7 lint-staged@^15.2.11
   ```

3. **Update package.json scripts:**
   ```json
   {
     "scripts": {
       "dev": "vite",
       "build": "tsc && vite build",
       "preview": "vite preview",
       "test": "jest",
       "test:watch": "jest --watch",
       "test:coverage": "jest --coverage",
       "lint": "eslint src --ext ts,tsx --report-unused-disable-directives --max-warnings 0",
       "lint:fix": "eslint src --ext ts,tsx --fix",
       "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
       "format:check": "prettier --check \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
       "type-check": "tsc --noEmit",
       "prepare": "husky install"
     }
   }
   ```

4. **Verify Installation:**
   ```bash
   npm run type-check
   npm run build
   ```

#### Acceptance Criteria:
- [ ] All dependencies install without conflicts
- [ ] `npm run build` completes successfully
- [ ] `npm run type-check` passes without errors
- [ ] Package.json contains all required scripts

---

## Phase 2: Code Quality and Testing Setup (4 hours)

### Task 2.1: ESLint and Prettier Configuration
**Estimated Time:** 1.5 hours  
**Priority:** High

#### Deliverables:
- [ ] ESLint configuration with React and TypeScript rules
- [ ] Prettier configuration for consistent formatting
- [ ] Linting passes without errors

#### Steps:
1. **Create .eslintrc.js:**
   ```javascript
   module.exports = {
     root: true,
     env: { browser: true, es2020: true },
     extends: [
       'eslint:recommended',
       '@typescript-eslint/recommended',
       'plugin:react-hooks/recommended',
       'plugin:react/recommended',
       'plugin:react/jsx-runtime',
     ],
     ignorePatterns: ['dist', '.eslintrc.js'],
     parser: '@typescript-eslint/parser',
     plugins: ['react-refresh'],
     rules: {
       'react-refresh/only-export-components': [
         'warn',
         { allowConstantExport: true },
       ],
       'react/prop-types': 'off',
       '@typescript-eslint/no-unused-vars': ['error', { argsIgnorePattern: '^_' }],
     },
     settings: {
       react: {
         version: 'detect',
       },
     },
   }
   ```

2. **Create .prettierrc:**
   ```json
   {
     "semi": true,
     "trailingComma": "es5",
     "singleQuote": true,
     "printWidth": 80,
     "tabWidth": 2,
     "useTabs": false
   }
   ```

3. **Create .eslintignore:**
   ```
   dist
   build
   node_modules
   *.config.js
   *.config.ts
   ```

4. **Test Linting:**
   ```bash
   npm run lint
   npm run format:check
   ```

#### Acceptance Criteria:
- [ ] ESLint configuration works with TypeScript and React
- [ ] Prettier formats code consistently
- [ ] `npm run lint` passes without errors
- [ ] `npm run format:check` passes

---

### Task 2.2: Jest and Testing Library Setup
**Estimated Time:** 2 hours  
**Priority:** High

#### Deliverables:
- [ ] Jest configuration for React Testing Library
- [ ] Sample test file that passes
- [ ] Coverage reporting configured

#### Steps:
1. **Create jest.config.js:**
   ```javascript
   module.exports = {
     testEnvironment: 'jsdom',
     setupFilesAfterEnv: ['<rootDir>/src/tests/setup.ts'],
     moduleNameMapping: {
       '^@/(.*)$': '<rootDir>/src/$1',
       '^@/components/(.*)$': '<rootDir>/src/components/$1',
       '^@/pages/(.*)$': '<rootDir>/src/pages/$1',
       '^@/hooks/(.*)$': '<rootDir>/src/hooks/$1',
       '^@/utils/(.*)$': '<rootDir>/src/utils/$1',
       '^@/api/(.*)$': '<rootDir>/src/api/$1',
       '^@/context/(.*)$': '<rootDir>/src/context/$1',
       '^@/styles/(.*)$': '<rootDir>/src/styles/$1',
     },
     collectCoverageFrom: [
       'src/**/*.{ts,tsx}',
       '!src/**/*.d.ts',
       '!src/main.tsx',
       '!src/vite-env.d.ts',
     ],
     coverageThreshold: {
       global: {
         branches: 90,
         functions: 90,
         lines: 90,
         statements: 90,
       },
     },
     testMatch: [
       '<rootDir>/src/**/__tests__/**/*.{ts,tsx}',
       '<rootDir>/src/**/*.{test,spec}.{ts,tsx}',
     ],
   };
   ```

2. **Create src/tests/setup.ts:**
   ```typescript
   import '@testing-library/jest-dom';
   ```

3. **Create sample test src/App.test.tsx:**
   ```typescript
   import { render, screen } from '@testing-library/react';
   import App from './App';

   test('renders learn react link', () => {
     render(<App />);
     const linkElement = screen.getByText(/vite \+ react/i);
     expect(linkElement).toBeInTheDocument();
   });
   ```

4. **Test Configuration:**
   ```bash
   npm test
   npm run test:coverage
   ```

#### Acceptance Criteria:
- [ ] Jest runs tests successfully
- [ ] Sample test passes
- [ ] Coverage report generates
- [ ] Path aliases work in tests
- [ ] Coverage threshold is set to 90%

---

### Task 2.3: Git Hooks and Pre-commit Setup
**Estimated Time:** 0.5 hours  
**Priority:** Medium

#### Deliverables:
- [ ] Husky configured for Git hooks
- [ ] Pre-commit hooks run linting and formatting
- [ ] Commit message validation (optional)

#### Steps:
1. **Initialize Husky:**
   ```bash
   npm run prepare
   npx husky add .husky/pre-commit "npx lint-staged"
   ```

2. **Configure lint-staged in package.json:**
   ```json
   {
     "lint-staged": {
       "src/**/*.{ts,tsx}": [
         "eslint --fix",
         "prettier --write"
       ],
       "src/**/*.{json,css,md}": [
         "prettier --write"
       ]
     }
   }
   ```

3. **Test Pre-commit Hook:**
   - Make a small change to a file
   - Commit and verify hooks run

#### Acceptance Criteria:
- [ ] Pre-commit hooks are installed
- [ ] Linting runs automatically on commit
- [ ] Formatting is applied automatically
- [ ] Commits are blocked if linting fails

---

## Phase 3: Material-UI and Theme Setup (3 hours)

### Task 3.1: Material-UI Integration
**Estimated Time:** 1.5 hours  
**Priority:** High

#### Deliverables:
- [ ] Material-UI theme provider configured
- [ ] Custom theme with brand colors
- [ ] Sample MUI components working

#### Steps:
1. **Create src/styles/theme.ts:**
   ```typescript
   import { createTheme } from '@mui/material/styles';

   export const theme = createTheme({
     palette: {
       primary: {
         main: '#1976d2',
         light: '#42a5f5',
         dark: '#1565c0',
       },
       secondary: {
         main: '#dc004e',
         light: '#ff5983',
         dark: '#9a0036',
       },
       background: {
         default: '#f5f5f5',
         paper: '#ffffff',
       },
     },
     typography: {
       fontFamily: '"Roboto", "Helvetica", "Arial", sans-serif',
       h1: {
         fontSize: '2.5rem',
         fontWeight: 600,
       },
       h2: {
         fontSize: '2rem',
         fontWeight: 600,
       },
     },
     components: {
       MuiButton: {
         styleOverrides: {
           root: {
             textTransform: 'none',
             borderRadius: 8,
           },
         },
       },
       MuiCard: {
         styleOverrides: {
           root: {
             borderRadius: 12,
             boxShadow: '0 2px 8px rgba(0,0,0,0.1)',
           },
         },
       },
     },
   });
   ```

2. **Update src/main.tsx:**
   ```typescript
   import React from 'react';
   import ReactDOM from 'react-dom/client';
   import { ThemeProvider } from '@mui/material/styles';
   import CssBaseline from '@mui/material/CssBaseline';
   import { theme } from '@/styles/theme';
   import App from './App';

   ReactDOM.createRoot(document.getElementById('root')!).render(
     <React.StrictMode>
       <ThemeProvider theme={theme}>
         <CssBaseline />
         <App />
       </ThemeProvider>
     </React.StrictMode>
   );
   ```

3. **Create sample component src/components/common/SampleCard.tsx:**
   ```typescript
   import { Card, CardContent, Typography, Button } from '@mui/material';
   import { Home as HomeIcon } from '@mui/icons-material';

   export const SampleCard = () => {
     return (
       <Card sx={{ maxWidth: 345, m: 2 }}>
         <CardContent>
           <Typography gutterBottom variant="h5" component="div">
             <HomeIcon sx={{ mr: 1, verticalAlign: 'middle' }} />
             PDF OCR Converter
           </Typography>
           <Typography variant="body2" color="text.secondary">
             Convert your PDF files to searchable documents with OCR technology.
           </Typography>
           <Button variant="contained" sx={{ mt: 2 }}>
             Get Started
           </Button>
         </CardContent>
       </Card>
     );
   };
   ```

4. **Update src/App.tsx to use MUI:**
   ```typescript
   import { Container, Box } from '@mui/material';
   import { SampleCard } from '@/components/common/SampleCard';

   function App() {
     return (
       <Container maxWidth="lg">
         <Box sx={{ py: 4 }}>
           <SampleCard />
         </Box>
       </Container>
     );
   }

   export default App;
   ```

#### Acceptance Criteria:
- [ ] Material-UI theme is applied globally
- [ ] Custom colors and typography work
- [ ] Material icons display correctly
- [ ] Sample component renders with MUI styling
- [ ] Responsive design works on different screen sizes

---

### Task 3.2: Responsive Design and Breakpoints
**Estimated Time:** 1 hour  
**Priority:** Medium

#### Deliverables:
- [ ] Responsive breakpoints configured
- [ ] Sample responsive component
- [ ] Mobile-first design approach

#### Steps:
1. **Update theme with custom breakpoints:**
   ```typescript
   // Add to src/styles/theme.ts
   export const theme = createTheme({
     // ... existing config
     breakpoints: {
       values: {
         xs: 0,
         sm: 600,
         md: 900,
         lg: 1200,
         xl: 1536,
       },
     },
   });
   ```

2. **Create responsive utility src/hooks/useResponsive.ts:**
   ```typescript
   import { useTheme } from '@mui/material/styles';
   import { useMediaQuery } from '@mui/material';

   export const useResponsive = () => {
     const theme = useTheme();
     
     const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
     const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
     const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
     
     return { isMobile, isTablet, isDesktop };
   };
   ```

3. **Update SampleCard to be responsive:**
   ```typescript
   import { useResponsive } from '@/hooks/useResponsive';

   export const SampleCard = () => {
     const { isMobile } = useResponsive();
     
     return (
       <Card sx={{ 
         maxWidth: isMobile ? '100%' : 345, 
         m: isMobile ? 1 : 2 
       }}>
         {/* ... rest of component */}
       </Card>
     );
   };
   ```

#### Acceptance Criteria:
- [ ] Responsive breakpoints work correctly
- [ ] Components adapt to different screen sizes
- [ ] Mobile-first approach is implemented
- [ ] useResponsive hook works properly

---

### Task 3.3: Toast Notifications Setup
**Estimated Time:** 0.5 hours  
**Priority:** Medium

#### Deliverables:
- [ ] React Toastify configured
- [ ] Toast container integrated with MUI theme
- [ ] Sample toast notifications working

#### Steps:
1. **Configure Toastify in src/main.tsx:**
   ```typescript
   import { ToastContainer } from 'react-toastify';
   import 'react-toastify/dist/ReactToastify.css';

   // Add to render function
   <React.StrictMode>
     <ThemeProvider theme={theme}>
       <CssBaseline />
       <App />
       <ToastContainer
         position="top-right"
         autoClose={5000}
         hideProgressBar={false}
         newestOnTop={false}
         closeOnClick
         rtl={false}
         pauseOnFocusLoss
         draggable
         pauseOnHover
         theme="light"
       />
     </ThemeProvider>
   </React.StrictMode>
   ```

2. **Create toast utility src/utils/toast.ts:**
   ```typescript
   import { toast } from 'react-toastify';

   export const showSuccess = (message: string) => {
     toast.success(message);
   };

   export const showError = (message: string) => {
     toast.error(message);
   };

   export const showInfo = (message: string) => {
     toast.info(message);
   };

   export const showWarning = (message: string) => {
     toast.warning(message);
   };
   ```

3. **Add sample toast to SampleCard:**
   ```typescript
   import { showSuccess } from '@/utils/toast';

   const handleGetStarted = () => {
     showSuccess('Welcome to PDF OCR Converter!');
   };

   // Update button
   <Button variant="contained" onClick={handleGetStarted} sx={{ mt: 2 }}>
     Get Started
   </Button>
   ```

#### Acceptance Criteria:
- [ ] Toast notifications display correctly
- [ ] Toast styling matches MUI theme
- [ ] Different toast types work (success, error, info, warning)
- [ ] Toast utility functions work properly

---

## Phase 4: Environment and Docker Configuration (3 hours)

### Task 4.1: Environment Variables Setup
**Estimated Time:** 1 hour  
**Priority:** High

#### Deliverables:
- [ ] Environment variables configuration
- [ ] TypeScript types for environment variables
- [ ] Different environment support

#### Steps:
1. **Create .env.example:**
   ```env
   # API Configuration
   VITE_API_BASE_URL=http://localhost:8000
   VITE_API_VERSION=v1

   # Google OAuth Configuration
   VITE_GOOGLE_CLIENT_ID=your_google_client_id_here

   # Application Configuration
   VITE_APP_NAME=PDF OCR Converter
   VITE_APP_VERSION=1.0.0

   # Feature Flags
   VITE_ENABLE_GOOGLE_DRIVE=true
   VITE_ENABLE_BATCH_PROCESSING=true

   # Development Configuration
   VITE_ENABLE_DEBUG=false
   ```

2. **Create .env.local (for development):**
   ```env
   VITE_API_BASE_URL=http://localhost:8000
   VITE_GOOGLE_CLIENT_ID=development_client_id
   VITE_ENABLE_DEBUG=true
   ```

3. **Create src/config/env.ts:**
   ```typescript
   interface EnvironmentConfig {
     apiBaseUrl: string;
     apiVersion: string;
     googleClientId: string;
     appName: string;
     appVersion: string;
     enableGoogleDrive: boolean;
     enableBatchProcessing: boolean;
     enableDebug: boolean;
   }

   export const env: EnvironmentConfig = {
     apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
     apiVersion: import.meta.env.VITE_API_VERSION || 'v1',
     googleClientId: import.meta.env.VITE_GOOGLE_CLIENT_ID || '',
     appName: import.meta.env.VITE_APP_NAME || 'PDF OCR Converter',
     appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',
     enableGoogleDrive: import.meta.env.VITE_ENABLE_GOOGLE_DRIVE === 'true',
     enableBatchProcessing: import.meta.env.VITE_ENABLE_BATCH_PROCESSING === 'true',
     enableDebug: import.meta.env.VITE_ENABLE_DEBUG === 'true',
   };

   // Validate required environment variables
   if (!env.googleClientId && import.meta.env.PROD) {
     throw new Error('VITE_GOOGLE_CLIENT_ID is required in production');
   }
   ```

4. **Update .gitignore:**
   ```
   # Environment variables
   .env.local
   .env.development.local
   .env.test.local
   .env.production.local
   ```

#### Acceptance Criteria:
- [ ] Environment variables are properly typed
- [ ] .env.example contains all required variables
- [ ] Environment validation works
- [ ] Different environments are supported

---

### Task 4.2: Docker Configuration
**Estimated Time:** 1.5 hours  
**Priority:** High

#### Deliverables:
- [ ] Multi-stage Dockerfile for development and production
- [ ] Docker Compose for local development
- [ ] Hot reload working in Docker

#### Steps:
1. **Create Dockerfile:**
   ```dockerfile
   # Development stage
   FROM node:20-alpine as development
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   EXPOSE 3000
   CMD ["npm", "run", "dev", "--", "--host"]

   # Build stage
   FROM node:20-alpine as build
   WORKDIR /app
   COPY package*.json ./
   RUN npm ci
   COPY . .
   RUN npm run build

   # Production stage
   FROM nginx:alpine as production
   COPY --from=build /app/build /usr/share/nginx/html
   COPY nginx.conf /etc/nginx/nginx.conf
   EXPOSE 80
   CMD ["nginx", "-g", "daemon off;"]
   ```

2. **Create nginx.conf:**
   ```nginx
   events {
     worker_connections 1024;
   }

   http {
     include /etc/nginx/mime.types;
     default_type application/octet-stream;

     server {
       listen 80;
       server_name localhost;
       root /usr/share/nginx/html;
       index index.html;

       location / {
         try_files $uri $uri/ /index.html;
       }

       location /api {
         proxy_pass http://backend:8000;
         proxy_set_header Host $host;
         proxy_set_header X-Real-IP $remote_addr;
       }
     }
   }
   ```

3. **Create docker-compose.yml:**
   ```yaml
   version: '3.8'

   services:
     frontend:
       build:
         context: .
         target: development
       ports:
         - "3000:3000"
       volumes:
         - .:/app
         - /app/node_modules
       environment:
         - VITE_API_BASE_URL=http://localhost:8000
       depends_on:
         - backend

     backend:
       image: python:3.11-alpine
       ports:
         - "8000:8000"
       command: echo "Backend service placeholder"

   networks:
     default:
       name: pdf-converter-network
   ```

4. **Create .dockerignore:**
   ```
   node_modules
   build
   dist
   .git
   .env.local
   .env.*.local
   npm-debug.log*
   yarn-debug.log*
   yarn-error.log*
   ```

5. **Test Docker Setup:**
   ```bash
   docker-compose up frontend
   ```

#### Acceptance Criteria:
- [ ] Docker builds successfully for development
- [ ] Docker Compose starts the application
- [ ] Hot reload works in Docker development mode
- [ ] Production build works with Nginx
- [ ] Environment variables work in Docker

---

### Task 4.3: Web Vitals and Performance Monitoring
**Estimated Time:** 0.5 hours  
**Priority:** Medium

#### Deliverables:
- [ ] Web Vitals monitoring configured
- [ ] Performance metrics logging
- [ ] Development performance insights

#### Steps:
1. **Create src/utils/performance.ts:**
   ```typescript
   import { getCLS, getFID, getFCP, getLCP, getTTFB } from 'web-vitals';

   export const reportWebVitals = (onPerfEntry?: (metric: any) => void) => {
     if (onPerfEntry && onPerfEntry instanceof Function) {
       getCLS(onPerfEntry);
       getFID(onPerfEntry);
       getFCP(onPerfEntry);
       getLCP(onPerfEntry);
       getTTFB(onPerfEntry);
     }
   };

   export const logPerformanceMetrics = () => {
     if (import.meta.env.DEV) {
       reportWebVitals((metric) => {
         console.log('Web Vital:', metric);
       });
     }
   };
   ```

2. **Update src/main.tsx:**
   ```typescript
   import { logPerformanceMetrics } from '@/utils/performance';

   // Add after render
   logPerformanceMetrics();
   ```

3. **Add performance budget to vite.config.ts:**
   ```typescript
   export default defineConfig({
     // ... existing config
     build: {
       outDir: 'build',
       sourcemap: true,
       rollupOptions: {
         output: {
           manualChunks: {
             vendor: ['react', 'react-dom'],
             mui: ['@mui/material', '@mui/icons-material'],
           },
         },
       },
     },
   });
   ```

#### Acceptance Criteria:
- [ ] Web Vitals are being measured
- [ ] Performance metrics are logged in development
- [ ] Bundle analysis is available
- [ ] Code splitting is configured

---

## Phase 5: Documentation and Final Testing (2 hours)

### Task 5.1: README and Documentation
**Estimated Time:** 1 hour  
**Priority:** High

#### Deliverables:
- [ ] Comprehensive README.md
- [ ] Development setup instructions
- [ ] Troubleshooting guide

#### Steps:
1. **Create README.md:**
   ```markdown
   # PDF OCR Converter - Frontend

   A modern React application for converting PDF files to searchable documents using OCR technology.

   ## Features

   - 🚀 Built with React 19 and TypeScript
   - 🎨 Material-UI v7 for consistent design
   - ⚡ Vite for fast development and builds
   - 🧪 Jest and React Testing Library for testing
   - 🔧 ESLint and Prettier for code quality
   - 🐳 Docker support for development and production
   - 📱 Responsive design with mobile-first approach

   ## Prerequisites

   - Node.js 20.x LTS
   - npm or yarn
   - Docker Desktop (optional)

   ## Getting Started

   ### Local Development

   1. Clone the repository:
      ```bash
      git clone <repository-url>
      cd frontend
      ```

   2. Install dependencies:
      ```bash
      npm install
      ```

   3. Copy environment variables:
      ```bash
      cp .env.example .env.local
      ```

   4. Start development server:
      ```bash
      npm run dev
      ```

   5. Open http://localhost:3000 in your browser

   ### Docker Development

   1. Start with Docker Compose:
      ```bash
      docker-compose up frontend
      ```

   2. Open http://localhost:3000 in your browser

   ## Available Scripts

   - `npm run dev` - Start development server
   - `npm run build` - Build for production
   - `npm run preview` - Preview production build
   - `npm test` - Run tests
   - `npm run test:coverage` - Run tests with coverage
   - `npm run lint` - Run ESLint
   - `npm run lint:fix` - Fix ESLint issues
   - `npm run format` - Format code with Prettier
   - `npm run type-check` - Check TypeScript types

   ## Project Structure

   ```
   src/
   ├── components/     # Reusable UI components
   ├── pages/         # Route-level components
   ├── hooks/         # Custom React hooks
   ├── context/       # React context providers
   ├── api/           # API client and services
   ├── utils/         # Utility functions
   ├── styles/        # Theme and styling
   ├── tests/         # Test utilities and setup
   └── assets/        # Static assets
   ```

   ## Environment Variables

   See `.env.example` for all available environment variables.

   ## Testing

   Run tests with:
   ```bash
   npm test
   ```

   Generate coverage report:
   ```bash
   npm run test:coverage
   ```

   ## Building for Production

   ```bash
   npm run build
   ```

   ## Troubleshooting

   ### Common Issues

   1. **Port 3000 already in use**
      - Change port in `vite.config.ts` or kill the process using port 3000

   2. **TypeScript errors after dependency updates**
      - Run `npm run type-check` to see detailed errors
      - Clear node_modules and reinstall: `rm -rf node_modules package-lock.json && npm install`

   3. **Docker build fails**
      - Ensure Docker Desktop is running
      - Check .dockerignore includes node_modules

   ## Contributing

   1. Follow the existing code style
   2. Run tests before committing
   3. Use conventional commit messages
   4. Ensure all linting passes

   ## License

   MIT License
   ```

#### Acceptance Criteria:
- [ ] README contains all necessary setup instructions
- [ ] All scripts are documented
- [ ] Troubleshooting section covers common issues
- [ ] Project structure is clearly explained

---

### Task 5.2: Final Testing and Validation
**Estimated Time:** 1 hour  
**Priority:** Critical

#### Deliverables:
- [ ] All tests passing
- [ ] Build process working
- [ ] Docker containers running
- [ ] Performance benchmarks met

#### Steps:
1. **Run Full Test Suite:**
   ```bash
   npm run type-check
   npm run lint
   npm run test:coverage
   npm run build
   ```

2. **Test Docker Setup:**
   ```bash
   docker-compose up --build
   # Verify application loads at http://localhost:3000
   ```

3. **Performance Testing:**
   ```bash
   npm run build
   npm run preview
   # Check Web Vitals in browser dev tools
   ```

4. **Accessibility Testing:**
   - Use browser dev tools to check accessibility
   - Verify keyboard navigation works
   - Check color contrast ratios

5. **Cross-browser Testing:**
   - Test in Chrome, Firefox, Safari, Edge
   - Test responsive design on different screen sizes

6. **Create Final Commit:**
   ```bash
   git add .
   git commit -m "feat: complete frontend application bootstrap

   - React 19 with TypeScript and Vite
   - Material-UI v7 with custom theme
   - Jest and React Testing Library setup
   - ESLint, Prettier, and Husky configuration
   - Docker development and production setup
   - Environment variables and configuration
   - Web Vitals performance monitoring
   - Comprehensive documentation"
   ```

#### Acceptance Criteria:
- [ ] All tests pass with 90%+ coverage
- [ ] Build completes without errors or warnings
- [ ] Docker containers start successfully
- [ ] Application loads and functions correctly
- [ ] Performance metrics meet requirements (FCP < 1.5s)
- [ ] Accessibility standards are met
- [ ] Cross-browser compatibility verified

---

## Completion Checklist

### Technical Requirements ✅
- [ ] React 19.2.0 with TypeScript 5.9.3
- [ ] Material-UI 7.3.5 with Emotion dependencies
- [ ] Vite 7.2.2 build tool configured
- [ ] Jest 30.2.0 and React Testing Library 16.3.0
- [ ] ESLint 9.39.1 and Prettier 3.6.2
- [ ] All dependencies at latest stable versions

### Code Quality ✅
- [ ] TypeScript strict mode enabled
- [ ] ESLint configuration with React rules
- [ ] Prettier formatting configured
- [ ] Pre-commit hooks with Husky and lint-staged
- [ ] 90%+ test coverage achieved

### Features ✅
- [ ] Material-UI theme with custom colors
- [ ] Responsive design with breakpoints
- [ ] Toast notifications configured
- [ ] Path aliases for absolute imports
- [ ] Environment variables with TypeScript types
- [ ] Web Vitals performance monitoring

### Infrastructure ✅
- [ ] Docker development and production setup
- [ ] Docker Compose for local development
- [ ] Hot reload working in development
- [ ] Production build optimized
- [ ] Nginx configuration for production

### Documentation ✅
- [ ] Comprehensive README.md
- [ ] Environment variables documented
- [ ] Development workflow explained
- [ ] Troubleshooting guide included
- [ ] All scripts documented

### Validation ✅
- [ ] All tests passing
- [ ] Build process working
- [ ] Docker containers running
- [ ] Performance benchmarks met
- [ ] Accessibility standards met
- [ ] Cross-browser compatibility verified

---

## Time Tracking Summary

| Phase | Estimated | Tasks |
|-------|-----------|-------|
| Phase 1: Project Initialization | 4 hours | Environment setup, TypeScript config, dependencies |
| Phase 2: Code Quality Setup | 4 hours | ESLint, Prettier, Jest, Git hooks |
| Phase 3: Material-UI Setup | 3 hours | Theme, responsive design, notifications |
| Phase 4: Environment & Docker | 3 hours | Environment variables, Docker, performance |
| Phase 5: Documentation & Testing | 2 hours | README, final validation |
| **Total** | **16 hours** | **13 tasks across 5 phases** |

## Next Steps

After completing this story:
1. **Story 01.1**: Basic Application Layout and Shell
2. **Story 02**: Backend Application Bootstrap (can be done in parallel)
3. **Story 03**: Google OAuth Authentication Frontend

The foundation is now ready for building the PDF OCR Converter application! 🚀