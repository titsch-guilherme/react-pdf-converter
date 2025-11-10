import {
  validateEmail,
  validateFileType,
  validateFileSize,
  validateFilename,
  validateJobId,
  validateFile,
  validateFiles,
  validateUrl,
  validateRequired,
  validateLength,
  validateRange,
} from './validators';

// Mock the constants
jest.mock('./constants', () => ({
  FILE_UPLOAD: {
    MAX_SIZE: 10485760, // 10MB
    MAX_FILES: 10,
    ALLOWED_TYPES: ['application/pdf'],
  },
  PATTERNS: {
    EMAIL: /^[^\s@]+@[^\s@]+\.[^\s@]+$/,
    FILENAME: /^[^<>:"/\\|?*]+$/,
    JOB_ID: /^[a-zA-Z0-9-_]+$/,
  },
}));

describe('Validators', () => {
  describe('validateEmail', () => {
    test('validates email correctly', () => {
      expect(validateEmail('test@example.com')).toEqual({ isValid: true });
      expect(validateEmail('user.name+tag@domain.co.uk')).toEqual({ isValid: true });
      
      expect(validateEmail('invalid-email')).toEqual({
        isValid: false,
        error: 'Invalid email format',
      });
      expect(validateEmail('')).toEqual({
        isValid: false,
        error: 'Email is required',
      });
      expect(validateEmail('test@')).toEqual({
        isValid: false,
        error: 'Invalid email format',
      });
    });
  });

  describe('validateFileType', () => {
    test('validates file type correctly', () => {
      const pdfFile = new File(['content'], 'test.pdf', { type: 'application/pdf' });
      const txtFile = new File(['content'], 'test.txt', { type: 'text/plain' });
      const docFile = new File(['content'], 'test.doc', { type: 'application/msword' });

      expect(validateFileType(pdfFile)).toEqual({ isValid: true });
      expect(validateFileType(txtFile)).toEqual({
        isValid: false,
        error: 'Invalid file type. Only application/pdf files are allowed.',
      });
      expect(validateFileType(docFile)).toEqual({
        isValid: false,
        error: 'Invalid file type. Only application/pdf files are allowed.',
      });
    });
  });

  describe('validateFileSize', () => {
    test('validates file size correctly', () => {
      const smallFile = new File(['small'], 'small.pdf', { type: 'application/pdf' });
      
      // Create a large file buffer for testing
      const largeBuffer = new ArrayBuffer(20971520); // 20MB
      const largeFile = new File([largeBuffer], 'large.pdf', { 
        type: 'application/pdf' 
      });

      expect(validateFileSize(smallFile)).toEqual({ isValid: true });
      expect(validateFileSize(largeFile)).toEqual({
        isValid: false,
        error: 'File size exceeds the maximum limit of 10.0MB.',
      });
    });

    test('handles edge cases', () => {
      // Exactly at the limit
      const exactSizeBuffer = new ArrayBuffer(10485760); // Exactly 10MB
      const exactSizeFile = new File([exactSizeBuffer], 'exact.pdf', { 
        type: 'application/pdf' 
      });
      
      expect(validateFileSize(exactSizeFile)).toEqual({ isValid: true });
    });
  });

  describe('validateFilename', () => {
    test('validates filename correctly', () => {
      expect(validateFilename('valid-filename.pdf')).toEqual({ isValid: true });
      expect(validateFilename('document_123.pdf')).toEqual({ isValid: true });
      expect(validateFilename('simple.pdf')).toEqual({ isValid: true });
      
      expect(validateFilename('invalid<filename>.pdf')).toEqual({
        isValid: false,
        error: 'Filename contains invalid characters',
      });
      expect(validateFilename('')).toEqual({
        isValid: false,
        error: 'Filename is required',
      });
      
      // Test very long filename
      const longFilename = 'a'.repeat(256) + '.pdf';
      expect(validateFilename(longFilename)).toEqual({
        isValid: false,
        error: 'Filename is too long (maximum 255 characters)',
      });
    });
  });

  describe('validateJobId', () => {
    test('validates job ID correctly', () => {
      expect(validateJobId('valid-job-id_123')).toEqual({ isValid: true });
      expect(validateJobId('abc123')).toEqual({ isValid: true });
      expect(validateJobId('job-123-abc')).toEqual({ isValid: true });
      
      expect(validateJobId('invalid job id')).toEqual({
        isValid: false,
        error: 'Invalid job ID format',
      });
      expect(validateJobId('')).toEqual({
        isValid: false,
        error: 'Job ID is required',
      });
      expect(validateJobId('invalid@job')).toEqual({
        isValid: false,
        error: 'Invalid job ID format',
      });
    });
  });

  describe('validateFile', () => {
    test('validates file correctly', () => {
      const validFile = new File(['content'], 'valid.pdf', { type: 'application/pdf' });
      const invalidTypeFile = new File(['content'], 'invalid.txt', { type: 'text/plain' });
      const invalidNameFile = new File(['content'], 'invalid<name>.pdf', { type: 'application/pdf' });

      expect(validateFile(validFile)).toEqual({ isValid: true });
      expect(validateFile(invalidTypeFile)).toEqual({
        isValid: false,
        error: 'Invalid file type. Only application/pdf files are allowed.',
      });
      expect(validateFile(invalidNameFile)).toEqual({
        isValid: false,
        error: 'Filename contains invalid characters',
      });
    });
  });

  describe('validateFiles', () => {
    test('validates multiple files correctly', () => {
      const file1 = new File(['content1'], 'file1.pdf', { type: 'application/pdf' });
      const file2 = new File(['content2'], 'file2.pdf', { type: 'application/pdf' });
      const duplicateFile = new File(['content3'], 'file1.pdf', { type: 'application/pdf' });
      const invalidFile = new File(['content4'], 'file3.txt', { type: 'text/plain' });

      expect(validateFiles([file1, file2])).toEqual({ isValid: true });
      
      expect(validateFiles([])).toEqual({
        isValid: false,
        error: 'No files selected',
      });
      
      expect(validateFiles([file1, duplicateFile])).toEqual({
        isValid: false,
        error: 'Duplicate filenames are not allowed',
      });
      
      expect(validateFiles([file1, invalidFile])).toEqual({
        isValid: false,
        error: 'File "file3.txt": Invalid file type. Only application/pdf files are allowed.',
      });
    });

    test('validates file count limits', () => {
      // Create 11 files (exceeds limit of 10)
      const files = Array.from({ length: 11 }, (_, i) => 
        new File(['content'], `file${i}.pdf`, { type: 'application/pdf' })
      );
      
      expect(validateFiles(files)).toEqual({
        isValid: false,
        error: 'You can upload a maximum of 10 files at once.',
      });
    });

    test('validates total file size - individual file size check first', () => {
      // Create files that individually exceed the limit (11MB each)
      // This should fail on individual file size validation first
      const oversizedBuffer = new ArrayBuffer(11534336); // 11MB each
      const oversizedFiles = Array.from({ length: 5 }, (_, i) => 
        new File([oversizedBuffer], `file${i}.pdf`, { type: 'application/pdf' })
      );
      
      // Should fail on individual file size check first
      expect(validateFiles(oversizedFiles)).toEqual({
        isValid: false,
        error: 'File "file0.pdf": File size exceeds the maximum limit of 10.0MB.',
      });
    });

    test('validates total file size - batch limit', () => {
      // Create files that individually are valid but together exceed total limit
      // Use files that are exactly at individual limit but exceed batch limit
      const maxIndividualSize = new ArrayBuffer(10485760); // 10MB each (at limit)
      const files = Array.from({ length: 11 }, (_, i) => 
        new File([maxIndividualSize], `file${i}.pdf`, { type: 'application/pdf' })
      );
      
      // Should fail on file count first (11 > 10)
      expect(validateFiles(files)).toEqual({
        isValid: false,
        error: 'You can upload a maximum of 10 files at once.',
      });
    });

    test('validates total file size - exactly at limits', () => {
      // Test exactly at the limits
      const maxIndividualSize = new ArrayBuffer(10485760); // 10MB each
      const files = Array.from({ length: 10 }, (_, i) => 
        new File([maxIndividualSize], `file${i}.pdf`, { type: 'application/pdf' })
      );
      
      // 10 files * 10MB = 100MB total, which should be exactly at the limit
      expect(validateFiles(files)).toEqual({ isValid: true });
    });
  });

  describe('validateUrl', () => {
    test('validates URL correctly', () => {
      expect(validateUrl('https://example.com')).toEqual({ isValid: true });
      expect(validateUrl('http://localhost:3000')).toEqual({ isValid: true });
      expect(validateUrl('ftp://files.example.com')).toEqual({ isValid: true });
      
      expect(validateUrl('invalid-url')).toEqual({
        isValid: false,
        error: 'Invalid URL format',
      });
      expect(validateUrl('')).toEqual({
        isValid: false,
        error: 'URL is required',
      });
      expect(validateUrl('not a url')).toEqual({
        isValid: false,
        error: 'Invalid URL format',
      });
    });
  });

  describe('validateRequired', () => {
    test('validates required field correctly', () => {
      expect(validateRequired('value', 'Field')).toEqual({ isValid: true });
      expect(validateRequired('  value  ', 'Field')).toEqual({ isValid: true });
      
      expect(validateRequired('', 'Field')).toEqual({
        isValid: false,
        error: 'Field is required',
      });
      expect(validateRequired('   ', 'Field')).toEqual({
        isValid: false,
        error: 'Field is required',
      });
      expect(validateRequired(null, 'Field')).toEqual({
        isValid: false,
        error: 'Field is required',
      });
      expect(validateRequired(undefined, 'Field')).toEqual({
        isValid: false,
        error: 'Field is required',
      });
    });
  });

  describe('validateLength', () => {
    test('validates string length correctly', () => {
      expect(validateLength('hello', 3, 10, 'Field')).toEqual({ isValid: true });
      expect(validateLength('abc', 3, 10, 'Field')).toEqual({ isValid: true });
      expect(validateLength('1234567890', 3, 10, 'Field')).toEqual({ isValid: true });
      
      expect(validateLength('hi', 3, 10, 'Field')).toEqual({
        isValid: false,
        error: 'Field must be at least 3 characters long',
      });
      expect(validateLength('very long string that exceeds limit', 3, 10, 'Field')).toEqual({
        isValid: false,
        error: 'Field must be no more than 10 characters long',
      });
    });
  });

  describe('validateRange', () => {
    test('validates number range correctly', () => {
      expect(validateRange(5, 1, 10, 'Field')).toEqual({ isValid: true });
      expect(validateRange(1, 1, 10, 'Field')).toEqual({ isValid: true });
      expect(validateRange(10, 1, 10, 'Field')).toEqual({ isValid: true });
      
      expect(validateRange(0, 1, 10, 'Field')).toEqual({
        isValid: false,
        error: 'Field must be at least 1',
      });
      expect(validateRange(15, 1, 10, 'Field')).toEqual({
        isValid: false,
        error: 'Field must be no more than 10',
      });
      expect(validateRange(-5, 1, 10, 'Field')).toEqual({
        isValid: false,
        error: 'Field must be at least 1',
      });
    });
  });
});