/**
 * Reusable confirmation dialog for destructive actions
 */
import { Modal, Text, Group, Button, Stack } from '@mantine/core';
import { IconAlertTriangle } from '@tabler/icons-react';

export interface ConfirmDialogProps {
  /** Whether the modal is opened */
  opened: boolean;
  /** Called when modal should close */
  onClose: () => void;
  /** Called when user confirms the action */
  onConfirm: () => void;
  /** Title of the dialog */
  title: string;
  /** Description/message of the dialog */
  message: string;
  /** Confirm button text */
  confirmText?: string;
  /** Cancel button text */
  cancelText?: string;
  /** Type of action (affects button color) */
  variant?: 'danger' | 'warning' | 'info';
  /** Whether the action is currently loading */
  loading?: boolean;
}

/**
 * ConfirmDialog provides a consistent confirmation UI for destructive actions.
 * Use this component when users need to confirm dangerous operations like deletions.
 *
 * @example
 * ```tsx
 * const [opened, { open, close }] = useDisclosure(false);
 *
 * <ConfirmDialog
 *   opened={opened}
 *   onClose={close}
 *   onConfirm={() => { deleteItem(); close(); }}
 *   title="Delete Item"
 *   message="Are you sure you want to delete this item? This action cannot be undone."
 *   variant="danger"
 * />
 * ```
 */
export function ConfirmDialog({
  opened,
  onClose,
  onConfirm,
  title,
  message,
  confirmText = 'Confirm',
  cancelText = 'Cancel',
  variant = 'danger',
  loading = false,
}: ConfirmDialogProps) {
  const handleConfirm = () => {
    onConfirm();
  };

  const getConfirmColor = () => {
    switch (variant) {
      case 'danger':
        return 'red';
      case 'warning':
        return 'yellow';
      case 'info':
        return 'blue';
      default:
        return 'red';
    }
  };

  return (
    <Modal
      opened={opened}
      onClose={onClose}
      title={title}
      centered
      size="md"
      closeOnClickOutside={!loading}
      closeOnEscape={!loading}
      withCloseButton={!loading}
    >
      <Stack gap="lg">
        <Group align="flex-start" gap="md">
          <IconAlertTriangle
            size={32}
            color={variant === 'danger' ? '#DC143C' : variant === 'warning' ? '#FF981F' : '#D4AF37'}
            aria-hidden="true"
          />
          <Text size="md" style={{ flex: 1 }}>
            {message}
          </Text>
        </Group>

        <Group justify="flex-end" gap="sm">
          <Button
            variant="default"
            onClick={onClose}
            disabled={loading}
            aria-label={`${cancelText} and close dialog`}
          >
            {cancelText}
          </Button>
          <Button
            color={getConfirmColor()}
            onClick={handleConfirm}
            loading={loading}
            aria-label={`${confirmText} action`}
          >
            {confirmText}
          </Button>
        </Group>
      </Stack>
    </Modal>
  );
}
