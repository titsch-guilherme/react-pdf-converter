import { toast } from 'react-toastify';
import {
  showSuccess,
  showError,
  showInfo,
  showWarning,
  showPromise,
  dismissToast,
  updateToast,
} from './toast';

// Mock react-toastify
jest.mock('react-toastify', () => ({
  toast: {
    success: jest.fn(),
    error: jest.fn(),
    info: jest.fn(),
    warning: jest.fn(),
    promise: jest.fn(),
    dismiss: jest.fn(),
    update: jest.fn(),
  },
}));

describe('Toast Utilities', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  describe('showSuccess', () => {
    test('calls toast.success with message and default options', () => {
      showSuccess('Success message');
      
      expect(toast.success).toHaveBeenCalledWith('Success message', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });

    test('calls toast.success with custom options', () => {
      const customOptions = { autoClose: 3000, position: 'bottom-left' as const };
      showSuccess('Success message', customOptions);
      
      expect(toast.success).toHaveBeenCalledWith('Success message', {
        position: 'bottom-left',
        autoClose: 3000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });
  });

  describe('showError', () => {
    test('calls toast.error with message and default options', () => {
      showError('Error message');
      
      expect(toast.error).toHaveBeenCalledWith('Error message', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });
  });

  describe('showInfo', () => {
    test('calls toast.info with message and default options', () => {
      showInfo('Info message');
      
      expect(toast.info).toHaveBeenCalledWith('Info message', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });
  });

  describe('showWarning', () => {
    test('calls toast.warning with message and default options', () => {
      showWarning('Warning message');
      
      expect(toast.warning).toHaveBeenCalledWith('Warning message', {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });
  });

  describe('showPromise', () => {
    test('calls toast.promise with promise and messages', () => {
      const promise = Promise.resolve('success');
      const messages = {
        pending: 'Loading...',
        success: 'Success!',
        error: 'Error!',
      };
      
      showPromise(promise, messages);
      
      expect(toast.promise).toHaveBeenCalledWith(promise, messages, {
        position: 'top-right',
        autoClose: 5000,
        hideProgressBar: false,
        closeOnClick: true,
        pauseOnHover: true,
        draggable: true,
        progress: undefined,
      });
    });
  });

  describe('dismissToast', () => {
    test('calls toast.dismiss with specific ID', () => {
      dismissToast('toast-id');
      
      expect(toast.dismiss).toHaveBeenCalledWith('toast-id');
    });

    test('calls toast.dismiss without ID to dismiss all', () => {
      dismissToast();
      
      expect(toast.dismiss).toHaveBeenCalledWith();
    });
  });

  describe('updateToast', () => {
    test('calls toast.update with ID and options', () => {
      const options = { render: 'Updated message' };
      updateToast('toast-id', options);
      
      expect(toast.update).toHaveBeenCalledWith('toast-id', options);
    });
  });
});