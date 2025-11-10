import {
  formatFileSize,
  formatDuration,
  formatProgress,
  formatRelativeTime,
  formatDate,
  truncateText,
  formatFilename,
  formatJobStatus,
  formatErrorMessage,
  formatNumber,
} from './formatters';

describe('Formatters', () => {
  describe('formatFileSize', () => {
    test('formats bytes correctly', () => {
      expect(formatFileSize(0)).toBe('0 Bytes');
      expect(formatFileSize(1024)).toBe('1 KB');
      expect(formatFileSize(1048576)).toBe('1 MB');
      expect(formatFileSize(1073741824)).toBe('1 GB');
      expect(formatFileSize(1536)).toBe('1.5 KB');
    });

    test('handles large file sizes', () => {
      expect(formatFileSize(1099511627776)).toBe('1 TB');
      expect(formatFileSize(2560000)).toBe('2.44 MB');
    });
  });

  describe('formatDuration', () => {
    test('formats duration correctly', () => {
      expect(formatDuration(1000)).toBe('1s');
      expect(formatDuration(60000)).toBe('1m 0s');
      expect(formatDuration(3661000)).toBe('1h 1m 1s');
      expect(formatDuration(90000)).toBe('1m 30s');
    });

    test('handles edge cases', () => {
      expect(formatDuration(0)).toBe('0s');
      expect(formatDuration(500)).toBe('0s');
      expect(formatDuration(7200000)).toBe('2h 0m 0s');
    });
  });

  describe('formatProgress', () => {
    test('formats progress percentage', () => {
      expect(formatProgress(0)).toBe('0%');
      expect(formatProgress(50.7)).toBe('51%');
      expect(formatProgress(100)).toBe('100%');
    });

    test('handles edge cases', () => {
      expect(formatProgress(-5)).toBe('-5%');
      expect(formatProgress(150)).toBe('150%');
    });
  });

  describe('formatRelativeTime', () => {
    beforeAll(() => {
      // Mock Date.now to return a fixed timestamp
      jest.useFakeTimers();
      jest.setSystemTime(new Date('2024-01-15T12:00:00Z'));
    });

    afterAll(() => {
      jest.useRealTimers();
    });

    test('formats relative time correctly', () => {
      const now = new Date('2024-01-15T12:00:00Z');
      const oneMinuteAgo = new Date('2024-01-15T11:59:00Z');
      const twoHoursAgo = new Date('2024-01-15T10:00:00Z');
      const threeDaysAgo = new Date('2024-01-12T12:00:00Z');

      expect(formatRelativeTime(new Date('2024-01-15T11:59:30Z'))).toBe('Just now');
      expect(formatRelativeTime(oneMinuteAgo)).toBe('1 minute ago');
      expect(formatRelativeTime(twoHoursAgo)).toBe('2 hours ago');
      expect(formatRelativeTime(threeDaysAgo)).toBe('3 days ago');
    });

    test('handles string dates', () => {
      expect(formatRelativeTime('2024-01-15T11:59:00Z')).toBe('1 minute ago');
    });
  });

  describe('formatDate', () => {
    test('formats date correctly', () => {
      const date = new Date('2024-01-15T10:30:00Z');
      const formatted = formatDate(date);
      expect(formatted).toContain('Jan');
      expect(formatted).toContain('15');
      expect(formatted).toContain('2024');
    });

    test('handles string dates', () => {
      const formatted = formatDate('2024-01-15T10:30:00Z');
      expect(formatted).toContain('Jan');
    });

    test('accepts custom options', () => {
      const date = new Date('2024-01-15T10:30:00Z');
      const formatted = formatDate(date, { year: 'numeric', month: 'long' });
      expect(formatted).toContain('January');
      expect(formatted).toContain('2024');
    });
  });

  describe('truncateText', () => {
    test('truncates text correctly', () => {
      expect(truncateText('Hello World', 5)).toBe('Hello...');
      expect(truncateText('Short', 10)).toBe('Short');
      expect(truncateText('', 5)).toBe('');
    });

    test('handles exact length', () => {
      expect(truncateText('Hello', 5)).toBe('Hello');
    });
  });

  describe('formatFilename', () => {
    test('formats filename correctly', () => {
      expect(formatFilename('document.pdf')).toBe('document');
      expect(formatFilename('very-long-filename-that-should-be-truncated.pdf', 10))
        .toBe('very-long-...');
    });

    test('handles files without extensions', () => {
      expect(formatFilename('document')).toBe('document');
    });

    test('handles multiple extensions', () => {
      expect(formatFilename('archive.tar.gz')).toBe('archive.tar');
    });
  });

  describe('formatJobStatus', () => {
    test('formats job status correctly', () => {
      expect(formatJobStatus('pending')).toBe('Pending');
      expect(formatJobStatus('processing')).toBe('Processing');
      expect(formatJobStatus('done')).toBe('Completed');
      expect(formatJobStatus('failed')).toBe('Failed');
      expect(formatJobStatus('unknown')).toBe('Unknown');
    });

    test('handles case variations', () => {
      expect(formatJobStatus('PENDING')).toBe('Pending');
      expect(formatJobStatus('Processing')).toBe('Processing');
    });
  });

  describe('formatErrorMessage', () => {
    test('formats error messages correctly', () => {
      expect(formatErrorMessage('String error')).toBe('String error');
      expect(formatErrorMessage(new Error('Error object'))).toBe('Error object');
      expect(formatErrorMessage({ message: 'Object with message' })).toBe('Object with message');
      expect(formatErrorMessage(null)).toBe('An unexpected error occurred');
      expect(formatErrorMessage(undefined)).toBe('An unexpected error occurred');
    });

    test('handles complex error objects', () => {
      const complexError = {
        message: 'Complex error',
        code: 500,
        details: 'Additional info'
      };
      expect(formatErrorMessage(complexError)).toBe('Complex error');
    });
  });

  describe('formatNumber', () => {
    test('formats numbers with thousand separators', () => {
      expect(formatNumber(1000)).toBe('1,000');
      expect(formatNumber(1234567)).toBe('1,234,567');
      expect(formatNumber(123)).toBe('123');
    });

    test('handles negative numbers', () => {
      expect(formatNumber(-1000)).toBe('-1,000');
    });

    test('handles decimal numbers', () => {
      expect(formatNumber(1234.56)).toBe('1,234.56');
    });
  });
});