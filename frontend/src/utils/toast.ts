import { toast, ToastOptions } from 'react-toastify';

const defaultOptions: ToastOptions = {
  position: 'top-right',
  autoClose: 5000,
  hideProgressBar: false,
  closeOnClick: true,
  pauseOnHover: true,
  draggable: true,
  progress: undefined,
};

export const showSuccess = (message: string, options?: ToastOptions) => {
  toast.success(message, { ...defaultOptions, ...options });
};

export const showError = (message: string, options?: ToastOptions) => {
  toast.error(message, { ...defaultOptions, ...options });
};

export const showInfo = (message: string, options?: ToastOptions) => {
  toast.info(message, { ...defaultOptions, ...options });
};

export const showWarning = (message: string, options?: ToastOptions) => {
  toast.warning(message, { ...defaultOptions, ...options });
};

export const showPromise = <T>(
  promise: Promise<T>,
  messages: {
    pending: string;
    success: string;
    error: string;
  },
  options?: ToastOptions
) => {
  return toast.promise(
    promise,
    messages,
    { ...defaultOptions, ...options }
  );
};

export const dismissToast = (toastId?: string | number) => {
  if (toastId) {
    toast.dismiss(toastId);
  } else {
    toast.dismiss();
  }
};

export const updateToast = (
  toastId: string | number,
  options: ToastOptions
) => {
  toast.update(toastId, options);
};