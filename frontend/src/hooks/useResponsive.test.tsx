import React from 'react';
import { renderHook } from '@testing-library/react';
import { ThemeProvider } from '@mui/material/styles';
import { useResponsive } from './useResponsive';
import { theme } from '@/styles/theme';

// Mock useMediaQuery
jest.mock('@mui/material', () => ({
  ...jest.requireActual('@mui/material'),
  useMediaQuery: jest.fn(),
}));

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <ThemeProvider theme={theme}>{children}</ThemeProvider>
);

describe('useResponsive Hook', () => {
  const mockUseMediaQuery = require('@mui/material').useMediaQuery as jest.Mock;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('returns correct values for desktop', () => {
    // Mock desktop breakpoints
    mockUseMediaQuery
      .mockReturnValueOnce(false) // isMobile (down sm)
      .mockReturnValueOnce(false) // isTablet (between sm and md)
      .mockReturnValueOnce(true)  // isDesktop (up md)
      .mockReturnValueOnce(false) // isSmallScreen (down md)
      .mockReturnValueOnce(true); // isLargeScreen (up lg)

    const { result } = renderHook(() => useResponsive(), { wrapper });

    expect(result.current).toEqual({
      isMobile: false,
      isTablet: false,
      isDesktop: true,
      isSmallScreen: false,
      isLargeScreen: true,
    });
  });

  test('returns correct values for mobile', () => {
    // Mock mobile breakpoints
    mockUseMediaQuery
      .mockReturnValueOnce(true)  // isMobile (down sm)
      .mockReturnValueOnce(false) // isTablet (between sm and md)
      .mockReturnValueOnce(false) // isDesktop (up md)
      .mockReturnValueOnce(true)  // isSmallScreen (down md)
      .mockReturnValueOnce(false); // isLargeScreen (up lg)

    const { result } = renderHook(() => useResponsive(), { wrapper });

    expect(result.current).toEqual({
      isMobile: true,
      isTablet: false,
      isDesktop: false,
      isSmallScreen: true,
      isLargeScreen: false,
    });
  });

  test('returns correct values for tablet', () => {
    // Mock tablet breakpoints
    mockUseMediaQuery
      .mockReturnValueOnce(false) // isMobile (down sm)
      .mockReturnValueOnce(true)  // isTablet (between sm and md)
      .mockReturnValueOnce(false) // isDesktop (up md)
      .mockReturnValueOnce(true)  // isSmallScreen (down md)
      .mockReturnValueOnce(false); // isLargeScreen (up lg)

    const { result } = renderHook(() => useResponsive(), { wrapper });

    expect(result.current).toEqual({
      isMobile: false,
      isTablet: true,
      isDesktop: false,
      isSmallScreen: true,
      isLargeScreen: false,
    });
  });
});