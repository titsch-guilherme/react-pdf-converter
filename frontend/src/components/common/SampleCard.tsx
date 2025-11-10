import { Card, CardContent, Typography, Button, Box } from '@mui/material';
import { CloudUpload as CloudUploadIcon, Security as SecurityIcon, Speed as SpeedIcon } from '@mui/icons-material';
import { useResponsive } from '@/hooks/useResponsive';
import { showSuccess } from '@/utils/toast';

export const SampleCard = () => {
  const { isMobile } = useResponsive();

  const handleGetStarted = () => {
    showSuccess('Welcome to PDF OCR Converter! 🎉');
  };

  const features = [
    {
      icon: <CloudUploadIcon color="primary" />,
      title: 'Easy Upload',
      description: 'Drag and drop multiple PDF files for batch processing',
    },
    {
      icon: <SecurityIcon color="primary" />,
      title: 'Secure Processing',
      description: 'Google OAuth authentication with secure file handling',
    },
    {
      icon: <SpeedIcon color="primary" />,
      title: 'Fast OCR',
      description: 'Advanced OCR technology for accurate text recognition',
    },
  ];

  return (
    <Card 
      sx={{ 
        maxWidth: isMobile ? '100%' : 600, 
        m: isMobile ? 1 : 2,
        transition: 'transform 0.2s ease-in-out',
        '&:hover': {
          transform: 'translateY(-4px)',
        },
      }}
    >
      <CardContent sx={{ p: 3 }}>
        <Typography 
          gutterBottom 
          variant="h4" 
          component="h1"
          sx={{ 
            textAlign: 'center',
            mb: 2,
            background: 'linear-gradient(45deg, #1976d2, #42a5f5)',
            backgroundClip: 'text',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontWeight: 'bold',
          }}
        >
          PDF OCR Converter
        </Typography>
        
        <Typography 
          variant="body1" 
          color="text.secondary" 
          sx={{ textAlign: 'center', mb: 3 }}
        >
          Transform your PDF files into searchable documents with our advanced OCR technology. 
          Upload multiple files, track conversion progress, and save results to Google Drive.
        </Typography>

        <Box sx={{ mb: 3 }}>
          {features.map((feature, index) => (
            <Box 
              key={index}
              sx={{ 
                display: 'flex', 
                alignItems: 'center', 
                mb: 2,
                p: 1,
                borderRadius: 1,
                '&:hover': {
                  backgroundColor: 'action.hover',
                },
              }}
            >
              <Box sx={{ mr: 2, display: 'flex', alignItems: 'center' }}>
                {feature.icon}
              </Box>
              <Box>
                <Typography variant="subtitle2" fontWeight="medium">
                  {feature.title}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {feature.description}
                </Typography>
              </Box>
            </Box>
          ))}
        </Box>

        <Box sx={{ textAlign: 'center' }}>
          <Button 
            variant="contained" 
            size="large"
            onClick={handleGetStarted}
            sx={{ 
              mt: 2,
              px: 4,
              py: 1.5,
              borderRadius: 2,
              textTransform: 'none',
              fontSize: '1.1rem',
              fontWeight: 600,
            }}
          >
            Get Started
          </Button>
        </Box>

        <Typography 
          variant="caption" 
          color="text.secondary" 
          sx={{ 
            display: 'block', 
            textAlign: 'center', 
            mt: 2,
            fontStyle: 'italic',
          }}
        >
          Built with React 19, Material-UI v7, and TypeScript
        </Typography>
      </CardContent>
    </Card>
  );
};

export default SampleCard;