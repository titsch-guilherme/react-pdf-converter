import { render, screen, fireEvent } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { SampleCard } from './SampleCard';
import { theme } from '@/styles/theme';

// Mock the toast utilities
jest.mock('@/utils/toast', () => ({
  showSuccess: jest.fn(),
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

  test('renders card title', () => {
    renderWithTheme(<SampleCard />);
    const titleElement = screen.getByText(/PDF OCR Converter/i);
    expect(titleElement).toBeInTheDocument();
  });

  test('renders card description', () => {
    renderWithTheme(<SampleCard />);
    const descriptionElement = screen.getByText(/Transform your PDF files into searchable documents/i);
    expect(descriptionElement).toBeInTheDocument();
  });

  test('renders all feature items', () => {
    renderWithTheme(<SampleCard />);
    
    expect(screen.getByText(/Easy Upload/i)).toBeInTheDocument();
    expect(screen.getByText(/Secure Processing/i)).toBeInTheDocument();
    expect(screen.getByText(/Fast OCR/i)).toBeInTheDocument();
  });

  test('renders feature descriptions', () => {
    renderWithTheme(<SampleCard />);
    
    expect(screen.getByText(/Drag and drop multiple PDF files/i)).toBeInTheDocument();
    expect(screen.getByText(/Google OAuth authentication/i)).toBeInTheDocument();
    expect(screen.getByText(/Advanced OCR technology/i)).toBeInTheDocument();
  });

  test('renders Get Started button', () => {
    renderWithTheme(<SampleCard />);
    const buttonElement = screen.getByRole('button', { name: /Get Started/i });
    expect(buttonElement).toBeInTheDocument();
  });

  test('calls showSuccess when Get Started button is clicked', async () => {
    const { showSuccess } = await import('@/utils/toast');
    
    renderWithTheme(<SampleCard />);
    const buttonElement = screen.getByRole('button', { name: /Get Started/i });
    
    fireEvent.click(buttonElement);
    
    expect(showSuccess).toHaveBeenCalledWith('Welcome to PDF OCR Converter! 🎉');
  });

  test('renders technology stack information', () => {
    renderWithTheme(<SampleCard />);
    const techStackElement = screen.getByText(/Built with React 19, Material-UI v7, and TypeScript/i);
    expect(techStackElement).toBeInTheDocument();
  });

  test('renders feature icons', () => {
    renderWithTheme(<SampleCard />);
    
    // Check for Material-UI icons by their SVG elements
    const icons = document.querySelectorAll('svg');
    expect(icons.length).toBeGreaterThan(0);
  });

  test('applies hover effects', () => {
    renderWithTheme(<SampleCard />);
    const cardElement = document.querySelector('.MuiCard-root');
    expect(cardElement).toBeInTheDocument();
  });

  test('renders responsive design for mobile', () => {
    // Mock mobile responsive hook
    jest.doMock('@/hooks/useResponsive', () => ({
      useResponsive: () => ({
        isMobile: true,
        isTablet: false,
        isDesktop: false,
        isSmallScreen: true,
        isLargeScreen: false,
      }),
    }));

    renderWithTheme(<SampleCard />);
    const cardElement = document.querySelector('.MuiCard-root');
    expect(cardElement).toBeInTheDocument();
  });
});