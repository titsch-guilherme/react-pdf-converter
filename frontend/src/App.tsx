import { Container, Box, CssBaseline } from '@mui/material';
import { ThemeProvider } from '@mui/material/styles';
import { ToastContainer } from 'react-toastify';
import { theme } from '@/styles/theme';
import { SampleCard } from '@/components/common';
import { logPerformanceMetrics } from '@/utils/performance';
import { env } from '@/config/env';
import 'react-toastify/dist/ReactToastify.css';

// Log performance metrics in development
if (env.enableDebug) {
  logPerformanceMetrics();
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Container maxWidth="lg">
        <Box 
          sx={{ 
            py: 4,
            minHeight: '100vh',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
          }}
        >
          <SampleCard />
        </Box>
      </Container>
      
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
        theme={theme.palette.mode}
        toastStyle={{
          borderRadius: theme.shape.borderRadius,
        }}
      />
    </ThemeProvider>
  );
}

export default App;