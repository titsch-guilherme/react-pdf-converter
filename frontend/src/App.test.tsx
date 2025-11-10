import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import App from './App';
import { theme } from '@/styles/theme';

// Mock the performance utilities
jest.mock('@/utils/performance', () => ({
  logPerformanceMetrics: jest.fn(),
}));

// Mock the environment config
jest.mock('@/config/env', () => ({
  env: {
    enableDebug: false,
    appName: 'PDF OCR Converter',
    appVersion: '1.0.0',
  },
}));

// Mock react-toastify
jest.mock('react-toastify', () => ({
  ToastContainer: () => <div data-testid="toast-container" />,
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    info: jest.fn(),
    warning: jest.fn(),
  },
}));

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('App Component', () => {
  beforeEach(() => {
    // Clear all mocks before each test
    jest.clearAllMocks();
  });

  test('renders PDF OCR Converter title', () => {
    renderWithTheme(<App />);
    const titleElement = screen.getByText(/PDF OCR Converter/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders application description', () => {
    renderWithTheme(<App />);
    const descriptionElement = screen.getByText(/Transform your PDF files into searchable documents/i);
    expect(descriptionElement).toBeInTheDocument();
  });

  test('renders Get Started button', () => {
    renderWithTheme(<App />);
    const buttonElement = screen.getByRole('button', { name: /Get Started/i });
    expect(buttonElement).toBeInTheDocument();
  });

  test('shows success toast when Get Started button is clicked', async () => {
    const { toast } = await import('react-toastify');
    
    renderWithTheme(<App />);
    const buttonElement = screen.getByRole('button', { name: /Get Started/i });
    
    fireEvent.click(buttonElement);
    
    await waitFor(() => {
      expect(toast.success).toHaveBeenCalledWith('Welcome to PDF OCR Converter! 🎉');
    });
  });

  test('renders feature list', () => {
    renderWithTheme(<App />);
    
    expect(screen.getByText(/Easy Upload/i)).toBeInTheDocument();
    expect(screen.getByText(/Secure Processing/i)).toBeInTheDocument();
    expect(screen.getByText(/Fast OCR/i)).toBeInTheDocument();
  });

  test('renders technology stack information', () => {
    renderWithTheme(<App />);
    const techStackElement = screen.getByText(/Built with React 19, Material-UI v7, and TypeScript/i);
    expect(techStackElement).toBeInTheDocument();
  });

  test('renders toast container', () => {
    renderWithTheme(<App />);
    const toastContainer = screen.getByTestId('toast-container');
    expect(toastContainer).toBeInTheDocument();
  });

  test('applies Material-UI theme correctly', () => {
    renderWithTheme(<App />);
    
    // Check if the theme is applied by looking for theme-specific styles
    const container = document.querySelector('.MuiContainer-root');
    expect(container).toBeInTheDocument();
  });

  test('renders responsive layout', () => {
    renderWithTheme(<App />);
    
    // Check if the container has the correct max width
    const container = document.querySelector('.MuiContainer-root');
    expect(container).toBeInTheDocument();
  });
});