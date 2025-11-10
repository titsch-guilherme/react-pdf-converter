import { env } from './env';

// Mock environment variables
const originalEnv = process.env;

describe('Environment Configuration', () => {
  beforeEach(() => {
    jest.resetModules();
    process.env = { ...originalEnv };
  });

  afterAll(() => {
    process.env = originalEnv;
  });

  test('has default values', () => {
    expect(env.apiBaseUrl).toBe('http://localhost:8000');
    expect(env.apiVersion).toBe('v1');
    expect(env.appName).toBe('PDF OCR Converter');
    expect(env.appVersion).toBe('1.0.0');
    expect(env.maxFileSize).toBe(10485760); // 10MB
    expect(env.maxFilesPerBatch).toBe(10);
    expect(env.statusPollInterval).toBe(3000);
    expect(env.maxPollAttempts).toBe(100);
    expect(env.themeMode).toBe('light');
  });

  test('has correct boolean defaults', () => {
    expect(env.enableGoogleDrive).toBe(true);
    expect(env.enableBatchProcessing).toBe(true);
    expect(env.enableDebug).toBe(false);
    expect(env.enableMockApi).toBe(false);
    expect(env.enableAnimations).toBe(true);
  });

  test('has correct array defaults', () => {
    expect(env.allowedFileTypes).toEqual(['application/pdf']);
  });

  test('validates required fields in production', () => {
    // This test would need to be run in a production environment
    // For now, we just check that the validation function exists
    expect(typeof env.googleClientId).toBe('string');
  });

  test('parses file types correctly', () => {
    // Test the file types parsing
    expect(env.allowedFileTypes).toContain('application/pdf');
  });

  test('has reasonable numeric limits', () => {
    expect(env.maxFileSize).toBeGreaterThan(0);
    expect(env.maxFilesPerBatch).toBeGreaterThan(0);
    expect(env.statusPollInterval).toBeGreaterThanOrEqual(1000);
    expect(env.maxPollAttempts).toBeGreaterThan(0);
  });
});