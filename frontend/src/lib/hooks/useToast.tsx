/**
 * Custom hook for displaying toast notifications
 * Wraps Mantine's notifications API with consistent styling
 */
import { notifications } from '@mantine/notifications';
import { IconCheck, IconX, IconAlertCircle, IconInfoCircle } from '@tabler/icons-react';

export type ToastType = 'success' | 'error' | 'warning' | 'info';

export interface ToastOptions {
  /** Toast message */
  message: string;
  /** Toast title (optional) */
  title?: string;
  /** Auto-close delay in ms (default: 4000, false to disable) */
  autoClose?: number | false;
  /** Toast ID for updating/dismissing */
  id?: string;
}

/**
 * Hook that provides consistent toast notification methods
 *
 * @example
 * ```tsx
 * const toast = useToast();
 *
 * toast.success({ message: 'Item saved successfully!' });
 * toast.error({ message: 'Failed to save item', title: 'Error' });
 * toast.warning({ message: 'This action is irreversible' });
 * toast.info({ message: 'Prices updated 5 minutes ago' });
 * ```
 */
export function useToast() {
  const success = ({ message, title = 'Success', autoClose = 4000, id }: ToastOptions) => {
    notifications.show({
      id,
      title,
      message,
      color: 'green',
      icon: <IconCheck size={18} />,
      autoClose,
      styles: {
        root: {
          backgroundColor: '#2B1B0E',
          borderColor: '#228B22',
        },
        title: {
          color: '#228B22',
        },
        description: {
          color: '#E8D4BB',
        },
      },
    });
  };

  const error = ({ message, title = 'Error', autoClose = 6000, id }: ToastOptions) => {
    notifications.show({
      id,
      title,
      message,
      color: 'red',
      icon: <IconX size={18} />,
      autoClose,
      styles: {
        root: {
          backgroundColor: '#2B1B0E',
          borderColor: '#DC143C',
        },
        title: {
          color: '#DC143C',
        },
        description: {
          color: '#E8D4BB',
        },
      },
    });
  };

  const warning = ({ message, title = 'Warning', autoClose = 5000, id }: ToastOptions) => {
    notifications.show({
      id,
      title,
      message,
      color: 'yellow',
      icon: <IconAlertCircle size={18} />,
      autoClose,
      styles: {
        root: {
          backgroundColor: '#2B1B0E',
          borderColor: '#FF981F',
        },
        title: {
          color: '#FF981F',
        },
        description: {
          color: '#E8D4BB',
        },
      },
    });
  };

  const info = ({ message, title = 'Info', autoClose = 4000, id }: ToastOptions) => {
    notifications.show({
      id,
      title,
      message,
      color: 'blue',
      icon: <IconInfoCircle size={18} />,
      autoClose,
      styles: {
        root: {
          backgroundColor: '#2B1B0E',
          borderColor: '#D4AF37',
        },
        title: {
          color: '#D4AF37',
        },
        description: {
          color: '#E8D4BB',
        },
      },
    });
  };

  const dismiss = (id: string) => {
    notifications.hide(id);
  };

  const dismissAll = () => {
    notifications.clean();
  };

  return {
    success,
    error,
    warning,
    info,
    dismiss,
    dismissAll,
  };
}
