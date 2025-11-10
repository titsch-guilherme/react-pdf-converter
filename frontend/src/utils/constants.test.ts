import {
  API_ENDPOINTS,
  FILE_UPLOAD,
  JOB_STATUS,
  POLLING,
  UI,
  ANIMATIONS,
  ERROR_MESSAGES,
  SUCCESS_MESSAGES,
  STORAGE_KEYS,
  GOOGLE_DRIVE,
  PATTERNS,
  FEATURES,
} from './constants';

// Mock the environment config
jest.mock('@/config/env', () => ({
  env: {
    maxFileSize: 10485760,
    maxFilesPerBatch: 10,
    allowedFileTypes: ['application/pdf'],
    statusPollInterval: 3000,
    maxPollAttempts: 100,
    enableGoogleDrive: true,
    enableBatchProcessing: true,
    enableDebug: false,
    enableMockApi: false,
    enableAnimations: true,
  },
}));

describe('Constants', () => {
  describe('API_ENDPOINTS', () => {
    test('has correct auth endpoints', () => {
      expect(API_ENDPOINTS.AUTH.VALIDATE).toBe('/auth/validate');
    });

    test('has correct convert endpoint', () => {
      expect(API_ENDPOINTS.CONVERT).toBe('/convert');
    });

    test('has correct status endpoints', () => {
      expect(API_ENDPOINTS.STATUS.SINGLE('job123')).toBe('/status/job123');
      expect(API_ENDPOINTS.STATUS.BATCH).toBe('/status');
    });

    test('has correct download endpoint', () => {
      expect(API_ENDPOINTS.DOWNLOAD('job123')).toBe('/download/job123');
    });
  });

  describe('FILE_UPLOAD', () => {
    test('has correct file upload constants', () => {
      expect(FILE_UPLOAD.MAX_SIZE).toBe(10485760);
      expect(FILE_UPLOAD.MAX_FILES).toBe(10);
      expect(FILE_UPLOAD.ALLOWED_TYPES).toEqual(['application/pdf']);
      expect(FILE_UPLOAD.CHUNK_SIZE).toBe(1024 * 1024);
    });
  });

  describe('JOB_STATUS', () => {
    test('has correct job status values', () => {
      expect(JOB_STATUS.PENDING).toBe('pending');
      expect(JOB_STATUS.PROCESSING).toBe('processing');
      expect(JOB_STATUS.DONE).toBe('done');
      expect(JOB_STATUS.FAILED).toBe('failed');
    });
  });

  describe('POLLING', () => {
    test('has correct polling configuration', () => {
      expect(POLLING.INTERVAL).toBe(3000);
      expect(POLLING.MAX_ATTEMPTS).toBe(100);
      expect(POLLING.BACKOFF_MULTIPLIER).toBe(1.5);
      expect(POLLING.MAX_INTERVAL).toBe(30000);
    });
  });

  describe('UI', () => {
    test('has correct UI constants', () => {
      expect(UI.DRAWER_WIDTH).toBe(240);
      expect(UI.HEADER_HEIGHT).toBe(64);
      expect(UI.FOOTER_HEIGHT).toBe(48);
      expect(UI.SIDEBAR_COLLAPSED_WIDTH).toBe(56);
    });
  });

  describe('ANIMATIONS', () => {
    test('has correct animation constants', () => {
      expect(ANIMATIONS.DURATION.SHORT).toBe(200);
      expect(ANIMATIONS.DURATION.MEDIUM).toBe(300);
      expect(ANIMATIONS.DURATION.LONG).toBe(500);
      
      expect(ANIMATIONS.EASING.EASE_IN).toBe('cubic-bezier(0.4, 0, 1, 1)');
      expect(ANIMATIONS.EASING.EASE_OUT).toBe('cubic-bezier(0, 0, 0.2, 1)');
      expect(ANIMATIONS.EASING.EASE_IN_OUT).toBe('cubic-bezier(0.4, 0, 0.2, 1)');
    });
  });

  describe('ERROR_MESSAGES', () => {
    test('has correct error messages', () => {
      expect(ERROR_MESSAGES.NETWORK).toBe('Network error. Please check your connection and try again.');
      expect(ERROR_MESSAGES.UNAUTHORIZED).toBe('You are not authorized to perform this action.');
      expect(ERROR_MESSAGES.FILE_TOO_LARGE).toBe('File size exceeds the maximum limit of 10.0MB.');
      expect(ERROR_MESSAGES.INVALID_FILE_TYPE).toBe('Invalid file type. Only PDF files are allowed.');
      expect(ERROR_MESSAGES.TOO_MANY_FILES).toBe('You can upload a maximum of 10 files at once.');
      expect(ERROR_MESSAGES.UPLOAD_FAILED).toBe('File upload failed. Please try again.');
      expect(ERROR_MESSAGES.CONVERSION_FAILED).toBe('File conversion failed. Please try again.');
      expect(ERROR_MESSAGES.DOWNLOAD_FAILED).toBe('File download failed. Please try again.');
      expect(ERROR_MESSAGES.GENERIC).toBe('An unexpected error occurred. Please try again.');
    });
  });

  describe('SUCCESS_MESSAGES', () => {
    test('has correct success messages', () => {
      expect(SUCCESS_MESSAGES.UPLOAD_SUCCESS).toBe('Files uploaded successfully!');
      expect(SUCCESS_MESSAGES.CONVERSION_SUCCESS).toBe('File conversion completed successfully!');
      expect(SUCCESS_MESSAGES.DOWNLOAD_SUCCESS).toBe('File downloaded successfully!');
      expect(SUCCESS_MESSAGES.DRIVE_UPLOAD_SUCCESS).toBe('Files uploaded to Google Drive successfully!');
    });
  });

  describe('STORAGE_KEYS', () => {
    test('has correct storage keys', () => {
      expect(STORAGE_KEYS.AUTH_TOKEN).toBe('pdf_ocr_auth_token');
      expect(STORAGE_KEYS.USER_PREFERENCES).toBe('pdf_ocr_user_preferences');
      expect(STORAGE_KEYS.THEME_MODE).toBe('pdf_ocr_theme_mode');
      expect(STORAGE_KEYS.RECENT_FILES).toBe('pdf_ocr_recent_files');
    });
  });

  describe('GOOGLE_DRIVE', () => {
    test('has correct Google Drive configuration', () => {
      expect(GOOGLE_DRIVE.FOLDER_NAME).toBe('Converted PDF Files');
      expect(GOOGLE_DRIVE.SCOPES).toEqual([
        'https://www.googleapis.com/auth/drive.file',
        'https://www.googleapis.com/auth/userinfo.profile',
        'https://www.googleapis.com/auth/userinfo.email',
      ]);
    });
  });

  describe('PATTERNS', () => {
    test('has correct regex patterns', () => {
      expect(PATTERNS.EMAIL.test('test@example.com')).toBe(true);
      expect(PATTERNS.EMAIL.test('invalid-email')).toBe(false);
      
      expect(PATTERNS.FILENAME.test('valid-filename.pdf')).toBe(true);
      expect(PATTERNS.FILENAME.test('invalid<filename>.pdf')).toBe(false);
      
      expect(PATTERNS.JOB_ID.test('valid-job-id_123')).toBe(true);
      expect(PATTERNS.JOB_ID.test('invalid job id')).toBe(false);
    });
  });

  describe('FEATURES', () => {
    test('has correct feature flags', () => {
      expect(FEATURES.GOOGLE_DRIVE).toBe(true);
      expect(FEATURES.BATCH_PROCESSING).toBe(true);
      expect(FEATURES.DEBUG_MODE).toBe(false);
      expect(FEATURES.MOCK_API).toBe(false);
      expect(FEATURES.ANIMATIONS).toBe(true);
    });
  });
});