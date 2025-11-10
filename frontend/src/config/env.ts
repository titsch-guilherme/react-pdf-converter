interface EnvironmentConfig {
  // API Configuration
  apiBaseUrl: string;
  apiVersion: string;
  
  // Google OAuth Configuration
  googleClientId: string;
  
  // Application Configuration
  appName: string;
  appVersion: string;
  
  // Feature Flags
  enableGoogleDrive: boolean;
  enableBatchProcessing: boolean;
  enableDebug: boolean;
  enableMockApi: boolean;
  
  // File Upload Configuration
  maxFileSize: number;
  maxFilesPerBatch: number;
  allowedFileTypes: string[];
  
  // Polling Configuration
  statusPollInterval: number;
  maxPollAttempts: number;
  
  // UI Configuration
  themeMode: 'light' | 'dark';
  enableAnimations: boolean;
}

const parseFileTypes = (types: string): string[] => {
  return types.split(',').map(type => type.trim());
};

const parseBoolean = (value: string | undefined, defaultValue: boolean): boolean => {
  if (value === undefined) return defaultValue;
  return value.toLowerCase() === 'true';
};

const parseNumber = (value: string | undefined, defaultValue: number): number => {
  if (value === undefined) return defaultValue;
  const parsed = parseInt(value, 10);
  return isNaN(parsed) ? defaultValue : parsed;
};

export const env: EnvironmentConfig = {
  // API Configuration
  apiBaseUrl: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  apiVersion: import.meta.env.VITE_API_VERSION || 'v1',
  
  // Google OAuth Configuration
  googleClientId: import.meta.env.VITE_GOOGLE_CLIENT_ID || '',
  
  // Application Configuration
  appName: import.meta.env.VITE_APP_NAME || 'PDF OCR Converter',
  appVersion: import.meta.env.VITE_APP_VERSION || '1.0.0',
  
  // Feature Flags
  enableGoogleDrive: parseBoolean(import.meta.env.VITE_ENABLE_GOOGLE_DRIVE, true),
  enableBatchProcessing: parseBoolean(import.meta.env.VITE_ENABLE_BATCH_PROCESSING, true),
  enableDebug: parseBoolean(import.meta.env.VITE_ENABLE_DEBUG, false),
  enableMockApi: parseBoolean(import.meta.env.VITE_ENABLE_MOCK_API, false),
  
  // File Upload Configuration
  maxFileSize: parseNumber(import.meta.env.VITE_MAX_FILE_SIZE, 10485760), // 10MB
  maxFilesPerBatch: parseNumber(import.meta.env.VITE_MAX_FILES_PER_BATCH, 10),
  allowedFileTypes: parseFileTypes(import.meta.env.VITE_ALLOWED_FILE_TYPES || 'application/pdf'),
  
  // Polling Configuration
  statusPollInterval: parseNumber(import.meta.env.VITE_STATUS_POLL_INTERVAL, 3000), // 3 seconds
  maxPollAttempts: parseNumber(import.meta.env.VITE_MAX_POLL_ATTEMPTS, 100),
  
  // UI Configuration
  themeMode: (import.meta.env.VITE_THEME_MODE as 'light' | 'dark') || 'light',
  enableAnimations: parseBoolean(import.meta.env.VITE_ENABLE_ANIMATIONS, true),
};

// Validate required environment variables
const validateEnvironment = () => {
  const errors: string[] = [];
  
  if (!env.googleClientId && import.meta.env.PROD) {
    errors.push('VITE_GOOGLE_CLIENT_ID is required in production');
  }
  
  if (!env.apiBaseUrl) {
    errors.push('VITE_API_BASE_URL is required');
  }
  
  if (env.maxFileSize <= 0) {
    errors.push('VITE_MAX_FILE_SIZE must be greater than 0');
  }
  
  if (env.maxFilesPerBatch <= 0) {
    errors.push('VITE_MAX_FILES_PER_BATCH must be greater than 0');
  }
  
  if (env.statusPollInterval < 1000) {
    errors.push('VITE_STATUS_POLL_INTERVAL must be at least 1000ms');
  }
  
  if (errors.length > 0) {
    throw new Error(`Environment validation failed:\n${errors.join('\n')}`);
  }
};

// Validate environment on module load
validateEnvironment();

export default env;