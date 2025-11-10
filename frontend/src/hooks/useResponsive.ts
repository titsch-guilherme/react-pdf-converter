import { useTheme } from '@mui/material/styles';
import { useMediaQuery } from '@mui/material';

export interface ResponsiveValues {
  isMobile: boolean;
  isTablet: boolean;
  isDesktop: boolean;
  isSmallScreen: boolean;
  isLargeScreen: boolean;
}

export const useResponsive = (): ResponsiveValues => {
  const theme = useTheme();
  
  const isMobile = useMediaQuery(theme.breakpoints.down('sm'));
  const isTablet = useMediaQuery(theme.breakpoints.between('sm', 'md'));
  const isDesktop = useMediaQuery(theme.breakpoints.up('md'));
  const isSmallScreen = useMediaQuery(theme.breakpoints.down('md'));
  const isLargeScreen = useMediaQuery(theme.breakpoints.up('lg'));
  
  return {
    isMobile,
    isTablet,
    isDesktop,
    isSmallScreen,
    isLargeScreen,
  };
};

export default useResponsive;