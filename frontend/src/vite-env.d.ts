/// <reference types="vite/client" />

interface ImportMetaEnv {
  // API Configuration
  readonly VITE_API_BASE_URL: string;
  readonly VITE_API_VERSION: string;
  
  // Google OAuth Configuration
  readonly VITE_GOOGLE_CLIENT_ID: string;
  
  // Application Configuration
  readonly VITE_APP_NAME: string;
  readonly VITE_APP_VERSION: string;
  
  // Feature Flags
  readonly VITE_ENABLE_GOOGLE_DRIVE: string;
  readonly VITE_ENABLE_BATCH_PROCESSING: string;
  readonly VITE_ENABLE_DEBUG: string;
  readonly VITE_ENABLE_MOCK_API: string;
  
  // File Upload Configuration
  readonly VITE_MAX_FILE_SIZE: string;
  readonly VITE_MAX_FILES_PER_BATCH: string;
  readonly VITE_ALLOWED_FILE_TYPES: string;
  
  // Polling Configuration
  readonly VITE_STATUS_POLL_INTERVAL: string;
  readonly VITE_MAX_POLL_ATTEMPTS: string;
  
  // UI Configuration
  readonly VITE_THEME_MODE: string;
  readonly VITE_ENABLE_ANIMATIONS: string;
}

interface ImportMeta {
  readonly env: ImportMetaEnv;
}