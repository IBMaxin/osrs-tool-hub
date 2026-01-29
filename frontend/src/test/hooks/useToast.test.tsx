import { renderHook } from '@testing-library/react';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import { MantineProvider } from '@mantine/core';
import { Notifications } from '@mantine/notifications';
import { useToast } from '../../lib/hooks/useToast';
import { notifications } from '@mantine/notifications';

// Mock the notifications module
vi.mock('@mantine/notifications', async () => {
  const actual = await vi.importActual('@mantine/notifications');
  return {
    ...actual,
    notifications: {
      show: vi.fn(),
      hide: vi.fn(),
      clean: vi.fn(),
    },
  };
});

const wrapper = ({ children }: { children: React.ReactNode }) => (
  <MantineProvider>
    <Notifications />
    {children}
  </MantineProvider>
);

describe('useToast', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('shows success toast with correct parameters', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.success({ message: 'Operation successful!' });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        message: 'Operation successful!',
        title: 'Success',
        color: 'green',
        autoClose: 4000,
      })
    );
  });

  it('shows error toast with correct parameters', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.error({ message: 'Something went wrong' });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        message: 'Something went wrong',
        title: 'Error',
        color: 'red',
        autoClose: 6000,
      })
    );
  });

  it('shows warning toast with correct parameters', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.warning({ message: 'Be careful!' });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        message: 'Be careful!',
        title: 'Warning',
        color: 'yellow',
        autoClose: 5000,
      })
    );
  });

  it('shows info toast with correct parameters', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.info({ message: 'For your information' });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        message: 'For your information',
        title: 'Info',
        color: 'blue',
        autoClose: 4000,
      })
    );
  });

  it('supports custom title', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.success({
      message: 'Done!',
      title: 'Custom Success',
    });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        title: 'Custom Success',
      })
    );
  });

  it('supports custom autoClose duration', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.success({
      message: 'Quick message',
      autoClose: 2000,
    });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        autoClose: 2000,
      })
    );
  });

  it('supports disabling autoClose', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.success({
      message: 'Persistent message',
      autoClose: false,
    });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        autoClose: false,
      })
    );
  });

  it('supports custom ID', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.success({
      message: 'Message with ID',
      id: 'custom-id',
    });

    expect(notifications.show).toHaveBeenCalledWith(
      expect.objectContaining({
        id: 'custom-id',
      })
    );
  });

  it('dismisses toast by ID', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.dismiss('toast-id');

    expect(notifications.hide).toHaveBeenCalledWith('toast-id');
  });

  it('dismisses all toasts', () => {
    const { result } = renderHook(() => useToast(), { wrapper });

    result.current.dismissAll();

    expect(notifications.clean).toHaveBeenCalled();
  });
});
