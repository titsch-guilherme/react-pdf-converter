import { FILE_UPLOAD, PATTERNS } from './constants';

export interface ValidationResult {
  isValid: boolean;
  error?: string;
}

/**
 * Validate email format
 */
export const validateEmail = (email: string): ValidationResult => {
  if (!email) {
    return { isValid: false, error: 'Email is required' };
  }
  
  if (!PATTERNS.EMAIL.test(email)) {
    return { isValid: false, error: 'Invalid email format' };
  }
  
  return { isValid: true };
};

/**
 * Validate file type
 */
export const validateFileType = (file: File): ValidationResult => {
  if (!FILE_UPLOAD.ALLOWED_TYPES.includes(file.type)) {
    return { 
      isValid: false, 
      error: `Invalid file type. Only ${FILE_UPLOAD.ALLOWED_TYPES.join(', ')} files are allowed.` 
    };
  }
  
  return { isValid: true };
};

/**
 * Validate file size
 */
export const validateFileSize = (file: File): ValidationResult => {
  if (file.size > FILE_UPLOAD.MAX_SIZE) {
    const maxSizeMB = (FILE_UPLOAD.MAX_SIZE / 1024 / 1024).toFixed(1);
    return { 
      isValid: false, 
      error: `File size exceeds the maximum limit of ${maxSizeMB}MB.` 
    };
  }
  
  return { isValid: true };
};

/**
 * Validate filename
 */
export const validateFilename = (filename: string): ValidationResult => {
  if (!filename) {
    return { isValid: false, error: 'Filename is required' };
  }
  
  if (!PATTERNS.FILENAME.test(filename)) {
    return { 
      isValid: false, 
      error: 'Filename contains invalid characters' 
    };
  }
  
  if (filename.length > 255) {
    return { 
      isValid: false, 
      error: 'Filename is too long (maximum 255 characters)' 
    };
  }
  
  return { isValid: true };
};

/**
 * Validate job ID format
 */
export const validateJobId = (jobId: string): ValidationResult => {
  if (!jobId) {
    return { isValid: false, error: 'Job ID is required' };
  }
  
  if (!PATTERNS.JOB_ID.test(jobId)) {
    return { 
      isValid: false, 
      error: 'Invalid job ID format' 
    };
  }
  
  return { isValid: true };
};

/**
 * Validate file for upload
 */
export const validateFile = (file: File): ValidationResult => {
  // Check file type
  const typeValidation = validateFileType(file);
  if (!typeValidation.isValid) {
    return typeValidation;
  }
  
  // Check file size
  const sizeValidation = validateFileSize(file);
  if (!sizeValidation.isValid) {
    return sizeValidation;
  }
  
  // Check filename
  const filenameValidation = validateFilename(file.name);
  if (!filenameValidation.isValid) {
    return filenameValidation;
  }
  
  return { isValid: true };
};

/**
 * Validate multiple files for batch upload
 */
export const validateFiles = (files: File[]): ValidationResult => {
  if (files.length === 0) {
    return { isValid: false, error: 'No files selected' };
  }
  
  if (files.length > FILE_UPLOAD.MAX_FILES) {
    return { 
      isValid: false, 
      error: `You can upload a maximum of ${FILE_UPLOAD.MAX_FILES} files at once.` 
    };
  }
  
  // Validate each file
  for (let i = 0; i < files.length; i++) {
    const fileValidation = validateFile(files[i]);
    if (!fileValidation.isValid) {
      return { 
        isValid: false, 
        error: `File "${files[i].name}": ${fileValidation.error}` 
      };
    }
  }
  
  // Check for duplicate filenames
  const filenames = files.map(file => file.name);
  const uniqueFilenames = new Set(filenames);
  if (filenames.length !== uniqueFilenames.size) {
    return { 
      isValid: false, 
      error: 'Duplicate filenames are not allowed' 
    };
  }
  
  // Check total size
  const totalSize = files.reduce((sum, file) => sum + file.size, 0);
  const maxTotalSize = FILE_UPLOAD.MAX_SIZE * FILE_UPLOAD.MAX_FILES;
  if (totalSize > maxTotalSize) {
    const maxTotalSizeMB = (maxTotalSize / 1024 / 1024).toFixed(1);
    return { 
      isValid: false, 
      error: `Total file size exceeds the maximum limit of ${maxTotalSizeMB}MB.` 
    };
  }
  
  return { isValid: true };
};

/**
 * Validate URL format
 */
export const validateUrl = (url: string): ValidationResult => {
  if (!url) {
    return { isValid: false, error: 'URL is required' };
  }
  
  try {
    new URL(url);
    return { isValid: true };
  } catch {
    return { isValid: false, error: 'Invalid URL format' };
  }
};

/**
 * Validate required field
 */
export const validateRequired = (value: string | null | undefined, fieldName: string): ValidationResult => {
  if (!value || value.trim() === '') {
    return { isValid: false, error: `${fieldName} is required` };
  }
  
  return { isValid: true };
};

/**
 * Validate string length
 */
export const validateLength = (
  value: string, 
  min: number, 
  max: number, 
  fieldName: string
): ValidationResult => {
  if (value.length < min) {
    return { 
      isValid: false, 
      error: `${fieldName} must be at least ${min} characters long` 
    };
  }
  
  if (value.length > max) {
    return { 
      isValid: false, 
      error: `${fieldName} must be no more than ${max} characters long` 
    };
  }
  
  return { isValid: true };
};

/**
 * Validate number range
 */
export const validateRange = (
  value: number, 
  min: number, 
  max: number, 
  fieldName: string
): ValidationResult => {
  if (value < min) {
    return { 
      isValid: false, 
      error: `${fieldName} must be at least ${min}` 
    };
  }
  
  if (value > max) {
    return { 
      isValid: false, 
      error: `${fieldName} must be no more than ${max}` 
    };
  }
  
  return { isValid: true };
};