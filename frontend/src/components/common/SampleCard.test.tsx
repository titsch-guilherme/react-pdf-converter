import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { SampleCard } from './SampleCard';
import { theme } from '@/styles/theme';

// Mock the toast utilities
jest.mock('@/utils/toast', () => ({
  showSuccess: jest.fn(),
}));

// Mock the performance utilities
jest.mock('@/utils/performance', () => ({
  measureCustomMetric: jest.fn(),
}));

// Mock the responsive hook
jest.mock('@/hooks/useResponsive', () => ({
  useResponsive: () => ({
    isMobile: false,
    isTablet: false,
    isDesktop: true,
    isSmallScreen: false,
    isLargeScreen: true,
  }),
}));

const renderWithTheme = (component: React.ReactElement) => {
  return render(
    <ThemeProvider theme={theme}>
      {component}
    </ThemeProvider>
  );
};

describe('SampleCard Component', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders correctly', () => {
    renderWithTheme(<SampleCard />);
    
    expect(screen.getByText('PDF OCR Converter')).toBeInTheDocument();
    expect(screen.getByText(/Transform your PDF files into searchable documents/)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /get started/i })).toBeInTheDocument();
  });

  test('displays feature list', () => {
    renderWithTheme(<SampleCard />);
    
    expect(screen.getByText('Easy Upload')).toBeInTheDocument();
    expect(screen.getByText('Secure Processing')).toBeInTheDocument();
    expect(screen.getByText('Fast OCR')).toBeInTheDocument();
    expect(screen.getByText('Drag and drop multiple PDF files for batch processing')).toBeInTheDocument();
  });

  test('handles get started button click', async () => {
    const { showSuccess } = require('@/utils/toast');
    
    renderWithTheme(<SampleCard />);
    
    const getStartedButton = screen.getByRole('button', { name: /get started/i });
    fireEvent.click(getStartedButton);
    
    await waitFor(() => {
      expect(showSuccess).toHaveBeenCalledWith('Welcome to PDF OCR Converter! 🎉');
    });
  });

  test('displays responsive design elements', () => {
    renderWithTheme(<SampleCard />);
    
    // Check for Material-UI components
    expect(screen.getByRole('button', { name: /get started/i })).toHaveClass('MuiButton-root');
    
    // Check for icons using data-testid
    const icons = document.querySelectorAll('[data-testid="CloudUploadIcon"], [data-testid="SecurityIcon"], [data-testid="SpeedIcon"]');
    expect(icons.length).toBe(3);
  });

  test('has proper accessibility attributes', () => {
    renderWithTheme(<SampleCard />);
    
    // Check for proper heading structure
    const heading = screen.getByRole('heading', { name: 'PDF OCR Converter' });
    expect(heading).toBeInTheDocument();
    expect(heading.tagName).toBe('H1');
    
    const button = screen.getByRole('button', { name: /get started/i });
    expect(button).toHaveAttribute('type');
  });

  test('displays technology stack information', () => {
    renderWithTheme(<SampleCard />);
    
    expect(screen.getByText('Built with React 19, Material-UI v7, and TypeScript')).toBeInTheDocument();
  });

  test('has hover effects and styling', () => {
    renderWithTheme(<SampleCard />);
    
    const card = document.querySelector('.MuiCard-root');
    expect(card).toBeInTheDocument();
    expect(card).toHaveStyle('transition: transform 0.2s ease-in-out');
  });
});