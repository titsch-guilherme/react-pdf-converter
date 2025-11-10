import { env } from '@/config/env';

// API Constants
export const API_ENDPOINTS = {
  AUTH: {
    VALIDATE: '/auth/validate',
  },
  CONVERT: '/convert',
  STATUS: {
    SINGLE: (jobId: string) => `/status/${jobId}`,
    BATCH: '/status',
  },
  DOWNLOAD: (jobId: string) => `/download/${jobId}`,
} as const;

// File Upload Constants
export const FILE_UPLOAD = {
  MAX_SIZE: env.maxFileSize,
  MAX_FILES: env.maxFilesPerBatch,
  ALLOWED_TYPES: env.allowedFileTypes,
  CHUNK_SIZE: 1024 * 1024, // 1MB chunks for large file uploads
} as const;

// Job Status Constants
export const JOB_STATUS = {
  PENDING: 'pending',
  PROCESSING: 'processing',
  DONE: 'done',
  FAILED: 'failed',
} as const;

export type JobStatus = typeof JOB_STATUS[keyof typeof JOB_STATUS];

// Polling Constants
export const POLLING = {
  INTERVAL: env.statusPollInterval,
  MAX_ATTEMPTS: env.maxPollAttempts,
  BACKOFF_MULTIPLIER: 1.5,
  MAX_INTERVAL: 30000, // 30 seconds max
} as const;

// UI Constants
export const UI = {
  DRAWER_WIDTH: 240,
  HEADER_HEIGHT: 64,
  FOOTER_HEIGHT: 48,
  SIDEBAR_COLLAPSED_WIDTH: 56,
} as const;

// Animation Constants
export const ANIMATIONS = {
  DURATION: {
    SHORT: 200,
    MEDIUM: 300,
    LONG: 500,
  },
  EASING: {
    EASE_IN: 'cubic-bezier(0.4, 0, 1, 1)',
    EASE_OUT: 'cubic-bezier(0, 0, 0.2, 1)',
    EASE_IN_OUT: 'cubic-bezier(0.4, 0, 0.2, 1)',
  },
} as const;

// Error Messages
export const ERROR_MESSAGES = {
  NETWORK: 'Network error. Please check your connection and try again.',
  UNAUTHORIZED: 'You are not authorized to perform this action.',
  FILE_TOO_LARGE: `File size exceeds the maximum limit of ${(FILE_UPLOAD.MAX_SIZE / 1024 / 1024).toFixed(1)}MB.`,
  INVALID_FILE_TYPE: 'Invalid file type. Only PDF files are allowed.',
  TOO_MANY_FILES: `You can upload a maximum of ${FILE_UPLOAD.MAX_FILES} files at once.`,
  UPLOAD_FAILED: 'File upload failed. Please try again.',
  CONVERSION_FAILED: 'File conversion failed. Please try again.',
  DOWNLOAD_FAILED: 'File download failed. Please try again.',
  GENERIC: 'An unexpected error occurred. Please try again.',
} as const;

// Success Messages
export const SUCCESS_MESSAGES = {
  UPLOAD_SUCCESS: 'Files uploaded successfully!',
  CONVERSION_SUCCESS: 'File conversion completed successfully!',
  DOWNLOAD_SUCCESS: 'File downloaded successfully!',
  DRIVE_UPLOAD_SUCCESS: 'Files uploaded to Google Drive successfully!',
} as const;

// Local Storage Keys
export const STORAGE_KEYS = {
  AUTH_TOKEN: 'pdf_ocr_auth_token',
  USER_PREFERENCES: 'pdf_ocr_user_preferences',
  THEME_MODE: 'pdf_ocr_theme_mode',
  RECENT_FILES: 'pdf_ocr_recent_files',
} as const;

// Google Drive Constants
export const GOOGLE_DRIVE = {
  FOLDER_NAME: 'Converted PDF Files',
  SCOPES: [
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/userinfo.profile',
    'https://www.googleapis.com/auth/userinfo.email',
  ],
} as const;

// Regex Patterns
export const PATTERNS = {
  EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
  FILENAME: /^[^<>:"/\\|?*]+$/,
  JOB_ID: /^[a-zA-Z0-9-_]+$/,
} as const;

// Feature Flags
export const FEATURES = {
  GOOGLE_DRIVE: env.enableGoogleDrive,
  BATCH_PROCESSING: env.enableBatchProcessing,
  DEBUG_MODE: env.enableDebug,
  MOCK_API: env.enableMockApi,
  ANIMATIONS: env.enableAnimations,
} as const;