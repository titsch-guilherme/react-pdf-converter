# Implementation Story 01: Frontend Application Bootstrap (Updated)

## Story Overview
**As a** developer  
**I want** a fully configured React.js frontend application with all necessary boilerplate, tooling, and scripts  
**So that** I can begin implementing PDF conversion features with a solid foundation

## SMART Criteria

### Specific
Create a React.js application with TypeScript, Material-UI, testing framework, linting, and all required development scripts configured and working.

### Measurable
- ✅ React 19.x application created with TypeScript
- ✅ Material-UI v7.x integrated with theme configuration
- ✅ ESLint and Prettier configured and passing
- ✅ Jest and React Testing Library setup with sample tests
- ✅ All npm scripts functional (start, build, test, lint, coverage)
- ✅ Project structure follows React code guidelines
- ✅ Environment configuration setup (.env files)
- ✅ Docker configuration for development

### Achievable
This is a standard React application setup using well-established tools and patterns.

### Relevant
Essential foundation for all subsequent frontend development work.

### Time-bound
**Estimated Duration:** 2 days  
**Sprint:** Sprint 1  
**Priority:** Critical (Blocker for other frontend stories)

## Technical Requirements

### Project Structure
```
frontend/
├── src/
│   ├── components/
│   │   └── common/
│   ├── pages/
│   ├── hooks/
│   ├── context/
│   ├── api/
│   ├── utils/
│   ├── styles/
│   ├── tests/
│   └── assets/
├── public/
├── package.json
├── tsconfig.json
├── .eslintrc.js
├── .prettierrc
├── jest.config.js
├── vite.config.ts (if using Vite)
├── Dockerfile
├── docker-compose.yml
└── .env.example
```

### Core Dependencies (Updated Versions)
- **React:** ^19.2.0 (latest stable)
- **React DOM:** ^19.2.0
- **TypeScript:** ^5.9.3
- **@mui/material:** ^7.3.5 (latest Material-UI)
- **@mui/icons-material:** ^7.3.5
- **@emotion/react:** ^11.14.0 (required for MUI v7)
- **@emotion/styled:** ^11.14.1 (required for MUI v7)
- **react-router-dom:** ^7.9.5 (latest stable)
- **axios:** ^1.13.2
- **react-dropzone:** ^14.3.8
- **react-toastify:** ^11.0.5 (updated from v9)

### Development Dependencies (Updated Versions)
- **@testing-library/react:** ^16.3.0
- **@testing-library/jest-dom:** ^6.9.1
- **@testing-library/user-event:** ^14.5.2
- **jest:** ^30.2.0
- **@types/jest:** ^30.0.0
- **eslint:** ^9.39.1
- **prettier:** ^3.6.2
- **@types/react:** ^19.2.2
- **@types/react-dom:** ^19.2.2
- **@types/node:** ^24.10.0
- **web-vitals:** ^5.1.0

### Build Tool Options

#### Option A: Vite (Recommended for new projects)
- **vite:** ^7.2.2
- **@vitejs/plugin-react:** ^5.1.0
- **@types/react:** ^19.2.2
- **@types/react-dom:** ^19.2.2

#### Option B: Create React App (Traditional approach)
- **react-scripts:** ^5.0.1 (if using CRA)

### Additional Development Tools
- **husky:** ^9.1.7 (Git hooks)
- **lint-staged:** ^15.2.11 (Staged file linting)
- **@typescript-eslint/eslint-plugin:** ^8.21.0
- **@typescript-eslint/parser:** ^8.21.0
- **eslint-plugin-react:** ^7.37.2
- **eslint-plugin-react-hooks:** ^5.1.0

## Acceptance Criteria

### AC1: Application Initialization
- [ ] React application created with **Vite (preferred)** or Create React App
- [ ] TypeScript configuration is properly set up with strict mode enabled
- [ ] Application starts successfully on `npm run dev` (Vite) or `npm start` (CRA)
- [ ] Application builds successfully with `npm run build`
- [ ] No TypeScript compilation errors
- [ ] Hot module replacement working in development

### AC2: UI Framework Integration
- [ ] Material-UI v7.3.5+ is installed and configured
- [ ] Emotion dependencies (@emotion/react, @emotion/styled) are properly installed
- [ ] Custom theme is created with primary/secondary colors
- [ ] Sample component using MUI components renders correctly
- [ ] Responsive design breakpoints are configured
- [ ] Material icons are available and working
- [ ] Theme provider is properly set up in App component

### AC3: Code Quality Tools
- [ ] ESLint configuration follows React code guidelines with TypeScript support
- [ ] Prettier configuration is set up with consistent formatting rules
- [ ] `npm run lint` passes without errors
- [ ] `npm run lint:fix` automatically fixes issues
- [ ] Pre-commit hooks are configured with husky and lint-staged
- [ ] TypeScript strict mode is enabled

### AC4: Testing Framework
- [ ] Jest is configured with React Testing Library
- [ ] Sample test file exists and passes
- [ ] `npm test` runs tests successfully
- [ ] `npm run test:coverage` generates coverage report
- [ ] Coverage threshold is set to 90%
- [ ] Testing utilities (@testing-library/user-event) are configured

### AC5: Project Structure
- [ ] Folder structure matches React code guidelines
- [ ] All required directories are created with index files
- [ ] Routing structure is prepared with react-router-dom v7
- [ ] Path aliases are configured in TypeScript/build tool
- [ ] Absolute imports are working (e.g., `import { Component } from 'components/Component'`)

### AC6: Environment Configuration
- [ ] `.env.example` file with all required variables
- [ ] Environment variables are properly typed with TypeScript
- [ ] Different environments supported (dev, test, prod)
- [ ] API base URL configuration is ready
- [ ] Vite environment variable naming convention followed (VITE_*)

### AC7: Docker Configuration
- [ ] Multi-stage Dockerfile for development and production
- [ ] Docker-compose.yml for local development
- [ ] Application runs successfully in Docker container
- [ ] Hot reload works in Docker development mode
- [ ] Production build optimization in Docker

### AC8: Documentation
- [ ] README.md with setup instructions for both Vite and CRA approaches
- [ ] Package.json scripts are documented
- [ ] Environment variables are documented
- [ ] Development workflow is documented
- [ ] Troubleshooting section included

### AC9: Performance and Modern Features (New)
- [ ] Web Vitals monitoring is set up
- [ ] Bundle analysis tools are configured
- [ ] Code splitting is prepared for future implementation
- [ ] Service worker registration is prepared (optional)
- [ ] Progressive Web App manifest is configured (optional)

## Package.json Scripts (Updated)

### For Vite Setup:
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
    "analyze": "npm run build && npx vite-bundle-analyzer dist/stats.html"
  }
}
```

### For Create React App Setup:
```json
{
  "scripts": {
    "start": "react-scripts start",
    "build": "react-scripts build",
    "test": "react-scripts test",
    "eject": "react-scripts eject",
    "test:coverage": "react-scripts test --coverage --watchAll=false",
    "lint": "eslint src --ext ts,tsx",
    "lint:fix": "eslint src --ext ts,tsx --fix",
    "format": "prettier --write \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "format:check": "prettier --check \"src/**/*.{ts,tsx,js,jsx,json,css,md}\"",
    "analyze": "npm run build && npx serve -s build"
  }
}
```

## Configuration Files

### TypeScript Configuration (tsconfig.json)
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

### Vite Configuration (vite.config.ts)
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

### ESLint Configuration (.eslintrc.js)
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

## Definition of Done
- [ ] All acceptance criteria are met
- [ ] Code review completed and approved
- [ ] All tests pass with 90%+ coverage
- [ ] Linting passes without warnings
- [ ] Application builds successfully for both development and production
- [ ] Docker container runs without errors
- [ ] Documentation is complete and accurate
- [ ] Performance benchmarks meet requirements (First Contentful Paint < 1.5s)
- [ ] Accessibility audit passes (WCAG 2.1 AA compliance)
- [ ] Story is deployed to development environment

## Dependencies
- None (This is the foundation story)

## Risks and Mitigation
- **Risk:** Version compatibility issues between dependencies
  - **Mitigation:** Use exact versions specified and test thoroughly
- **Risk:** Material-UI v7 breaking changes from v5
  - **Mitigation:** Follow official migration guide and test all components
- **Risk:** React 19 compatibility issues with third-party libraries
  - **Mitigation:** Verify compatibility of all dependencies before implementation
- **Risk:** Docker configuration complexity with new build tools
  - **Mitigation:** Start with simple configuration, use multi-stage builds

## Migration Notes from Previous Versions

### Material-UI v5 to v7 Changes:
- Emotion dependencies are now required
- Some breaking changes in theming system
- Updated component APIs

### React 18 to 19 Changes:
- New JSX transform is default
- Improved TypeScript support
- New concurrent features

### Build Tool Considerations:
- **Vite is recommended** for new projects due to faster development server and build times
- Create React App is still supported but consider migration path to Vite
- Vite requires different environment variable naming (VITE_ prefix)

## Notes
- This story establishes the foundation for all frontend development
- **Vite is preferred over Create React App** for better performance and modern tooling
- Focus on getting a clean, working setup rather than adding features
- Ensure all team members can run the application locally
- Material-UI v7 requires Emotion dependencies - ensure they're included
- React 19 is the latest stable version - use it for new projects
- Consider Progressive Web App features for future enhancement