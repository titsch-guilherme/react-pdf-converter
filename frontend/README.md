# PDF OCR Converter - Frontend

A modern React application for converting PDF files to searchable documents using OCR technology.

## 🚀 Features

- **Modern Stack**: Built with React 19, TypeScript 5.9, and Vite 7.2
- **UI Framework**: Material-UI v7 with custom theming and responsive design
- **Code Quality**: ESLint, Prettier, and comprehensive testing setup
- **Performance**: Web Vitals monitoring and optimized builds
- **Development**: Hot reload, path aliases, and Docker support
- **Accessibility**: WCAG 2.1 AA compliant with keyboard navigation

## 📋 Prerequisites

- Node.js 20.x LTS or higher
- npm 10.x or higher
- Docker Desktop (optional, for containerized development)

## 🛠️ Getting Started

### Local Development

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Copy environment variables:**
   ```bash
   cp .env.example .env.local
   ```

4. **Start development server:**
   ```bash
   npm run dev
   ```

5. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

### Docker Development

1. **Start with Docker Compose:**
   ```bash
   docker-compose up frontend
   ```

2. **Open your browser:**
   Navigate to [http://localhost:3000](http://localhost:3000)

## 📜 Available Scripts

| Script | Description |
|--------|-------------|
| `npm run dev` | Start development server with hot reload |
| `npm run build` | Build for production |
| `npm run preview` | Preview production build locally |
| `npm test` | Run tests in watch mode |
| `npm run test:coverage` | Run tests with coverage report |
| `npm run lint` | Run ESLint |
| `npm run lint:fix` | Fix ESLint issues automatically |
| `npm run format` | Format code with Prettier |
| `npm run format:check` | Check code formatting |
| `npm run type-check` | Check TypeScript types |
| `npm run analyze` | Analyze bundle size |

## 📁 Project Structure

```
src/
├── components/          # Reusable UI components
│   ├── common/         # Shared components
│   ├── auth/           # Authentication components
│   ├── upload/         # File upload components
│   └── status/         # Status tracking components
├── pages/              # Route-level components
├── hooks/              # Custom React hooks
├── context/            # React context providers
├── api/                # API client and services
├── utils/              # Utility functions
├── styles/             # Theme and styling
├── tests/              # Test utilities and setup
├── assets/             # Static assets
└── config/             # Configuration files
```

## 🔧 Configuration

### Environment Variables

Copy `.env.example` to `.env.local` and configure:

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
VITE_ENABLE_DEBUG=false
```

### Path Aliases

The project uses TypeScript path aliases for cleaner imports:

```typescript
import { Component } from '@/components/Component';
import { useHook } from '@/hooks/useHook';
import { utility } from '@/utils/utility';
```

## 🧪 Testing

### Running Tests

```bash
# Run tests in watch mode
npm test

# Run tests with coverage
npm run test:coverage

# Run tests in CI mode
npm test -- --watchAll=false
```

### Test Structure

- **Unit Tests**: Component and utility function tests
- **Integration Tests**: API integration and state management
- **Coverage**: 90% threshold for branches, functions, lines, and statements

### Writing Tests

```typescript
import { render, screen } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { MyComponent } from './MyComponent';
import { theme } from '@/styles/theme';

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

test('renders component correctly', () => {
  renderWithTheme(<MyComponent />);
  expect(screen.getByText('Expected Text')).toBeInTheDocument();
});
```

## 🏗️ Building for Production

### Local Build

```bash
npm run build
```

### Docker Production Build

```bash
docker-compose --profile production up frontend-prod
```

### Build Optimization

- **Code Splitting**: Automatic vendor and route-based splitting
- **Tree Shaking**: Unused code elimination
- **Asset Optimization**: Image and font optimization
- **Bundle Analysis**: Use `npm run analyze` to inspect bundle size

## 🐳 Docker Support

### Development Container

```dockerfile
# Hot reload enabled
docker-compose up frontend
```

### Production Container

```dockerfile
# Nginx-served static files
docker-compose --profile production up frontend-prod
```

### Multi-stage Build

The Dockerfile includes three stages:
1. **Development**: Hot reload with Vite
2. **Build**: Production build generation
3. **Production**: Nginx-served static files

## 🎨 Theming and Styling

### Material-UI Theme

The application uses a custom Material-UI theme with:

- **Primary Color**: #1976d2 (Blue)
- **Secondary Color**: #dc004e (Pink)
- **Typography**: Roboto font family
- **Responsive Breakpoints**: xs, sm, md, lg, xl
- **Custom Components**: Styled buttons, cards, and form elements

### Responsive Design

```typescript
import { useResponsive } from '@/hooks/useResponsive';

const MyComponent = () => {
  const { isMobile, isTablet, isDesktop } = useResponsive();
  
  return (
    <Box sx={{ 
      padding: isMobile ? 1 : 2,
      flexDirection: isMobile ? 'column' : 'row' 
    }}>
      {/* Responsive content */}
    </Box>
  );
};
```

## 📊 Performance Monitoring

### Web Vitals

The application monitors Core Web Vitals:

- **First Contentful Paint (FCP)**: < 1.5s
- **Largest Contentful Paint (LCP)**: < 2.5s
- **First Input Delay (FID)**: < 100ms
- **Cumulative Layout Shift (CLS)**: < 0.1

### Performance Budget

```typescript
import { checkPerformanceBudget } from '@/utils/performance';

// Automatically checks performance thresholds
checkPerformanceBudget(metrics);
```

## 🔍 Troubleshooting

### Common Issues

1. **Port 3000 already in use**
   ```bash
   # Kill process using port 3000
   lsof -ti:3000 | xargs kill -9
   
   # Or change port in vite.config.ts
   server: { port: 3001 }
   ```

2. **TypeScript errors after dependency updates**
   ```bash
   # Clear cache and reinstall
   rm -rf node_modules package-lock.json
   npm install
   npm run type-check
   ```

3. **Docker build fails**
   ```bash
   # Ensure Docker Desktop is running
   docker --version
   
   # Clear Docker cache
   docker system prune -a
   ```

4. **Tests failing after updates**
   ```bash
   # Clear Jest cache
   npm test -- --clearCache
   
   # Update snapshots if needed
   npm test -- --updateSnapshot
   ```

### Development Tips

- **Hot Reload Issues**: Restart dev server if changes aren't reflected
- **Import Errors**: Check path aliases in `tsconfig.json` and `vite.config.ts`
- **Styling Issues**: Verify Material-UI theme provider wraps components
- **Performance**: Use React DevTools Profiler for component optimization

## 🤝 Contributing

### Code Style

1. **Follow existing patterns**: Use established component and hook patterns
2. **TypeScript**: Use strict typing, avoid `any` types
3. **Testing**: Write tests for new components and utilities
4. **Documentation**: Update README for new features

### Commit Guidelines

```bash
# Use conventional commits
git commit -m "feat: add new component"
git commit -m "fix: resolve styling issue"
git commit -m "docs: update README"
```

### Pre-commit Hooks

The project uses Husky and lint-staged for:
- **Linting**: ESLint checks on staged files
- **Formatting**: Prettier formatting on staged files
- **Type Checking**: TypeScript compilation check

## 📚 Technology Stack

| Technology | Version | Purpose |
|------------|---------|---------|
| React | ^19.2.0 | UI framework |
| TypeScript | ^5.9.3 | Type safety |
| Vite | ^7.2.2 | Build tool |
| Material-UI | ^7.3.5 | UI components |
| React Router | ^7.9.5 | Routing |
| Axios | ^1.13.2 | HTTP client |
| Jest | ^30.2.0 | Testing framework |
| ESLint | ^9.39.1 | Code linting |
| Prettier | ^3.6.2 | Code formatting |

## 📄 License

MIT License - see [LICENSE](../LICENSE) file for details.

## 🆘 Support

For support and questions:

1. **Documentation**: Check this README and inline code comments
2. **Issues**: Create GitHub issues for bugs and feature requests
3. **Development**: Use the development environment for testing

---

**Built with ❤️ using React 19, Material-UI v7, and TypeScript**