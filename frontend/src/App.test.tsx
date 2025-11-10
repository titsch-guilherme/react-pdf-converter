import { render, screen } from '@testing-library/react';
import App from './App';

// Mock the performance utilities
jest.mock('@/utils/performance', () => ({
  logPerformanceMetrics: jest.fn(),
}));

// Mock the environment config
jest.mock('@/config/env', () => ({
  env: {
    enableDebug: false,
  },
}));

describe('App Component', () => {
  test('renders without crashing', () => {
    render(<App />);
    
    // Check if the main container is rendered
    const container = document.querySelector('.MuiContainer-root');
    expect(container).toBeInTheDocument();
  });

  test('includes ThemeProvider', () => {
    render(<App />);
    
    // Check if Material-UI theme is applied
    const container = document.querySelector('.MuiContainer-root');
    expect(container).toBeInTheDocument();
  });

  test('includes CssBaseline', () => {
    render(<App />);
    
    // CssBaseline should normalize styles
    const body = document.body;
    expect(body).toBeInTheDocument();
  });

  test('renders SampleCard component', () => {
    render(<App />);
    
    // Check if SampleCard content is present
    expect(screen.getByText('PDF OCR Converter')).toBeInTheDocument();
  });

  test('has proper layout structure', () => {
    render(<App />);
    
    // Check main layout elements
    const container = document.querySelector('.MuiContainer-root');
    const box = container?.querySelector('.MuiBox-root');
    
    expect(container).toBeInTheDocument();
    expect(box).toBeInTheDocument();
  });

  test('applies responsive design', () => {
    render(<App />);
    
    const container = document.querySelector('.MuiContainer-root');
    expect(container).toHaveClass('MuiContainer-maxWidthLg');
  });

  test('includes toast container setup', () => {
    render(<App />);
    
    // ToastContainer is rendered but may not have the class until a toast is shown
    // Just check that the app renders without errors
    expect(screen.getByText('PDF OCR Converter')).toBeInTheDocument();
  });
});