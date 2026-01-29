import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { MantineProvider } from '@mantine/core';
import { ConfirmDialog } from '../../lib/components/ConfirmDialog';

const renderWithProviders = (ui: React.ReactElement) => {
  return render(<MantineProvider>{ui}</MantineProvider>);
};

describe('ConfirmDialog', () => {
  const defaultProps = {
    opened: true,
    onClose: vi.fn(),
    onConfirm: vi.fn(),
    title: 'Delete Item',
    message: 'Are you sure you want to delete this item?',
  };

  it('renders with title and message', () => {
    renderWithProviders(<ConfirmDialog {...defaultProps} />);
    
    expect(screen.getByText('Delete Item')).toBeInTheDocument();
    expect(screen.getByText('Are you sure you want to delete this item?')).toBeInTheDocument();
  });

  it('shows warning icon', () => {
    renderWithProviders(<ConfirmDialog {...defaultProps} />);
    
    // Alert triangle icon should be present
    const icon = document.querySelector('[aria-hidden="true"]');
    expect(icon).toBeInTheDocument();
  });

  it('calls onConfirm when confirm button is clicked', async () => {
    const user = userEvent.setup();
    const onConfirm = vi.fn();
    
    renderWithProviders(
      <ConfirmDialog {...defaultProps} onConfirm={onConfirm} />
    );
    
    const confirmButton = screen.getByRole('button', { name: /confirm action/i });
    await user.click(confirmButton);
    
    expect(onConfirm).toHaveBeenCalledTimes(1);
  });

  it('calls onClose when cancel button is clicked', async () => {
    const user = userEvent.setup();
    const onClose = vi.fn();
    
    renderWithProviders(
      <ConfirmDialog {...defaultProps} onClose={onClose} />
    );
    
    const cancelButton = screen.getByRole('button', { name: /cancel and close dialog/i });
    await user.click(cancelButton);
    
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('supports custom button text', () => {
    renderWithProviders(
      <ConfirmDialog
        {...defaultProps}
        confirmText="Delete"
        cancelText="Keep"
      />
    );
    
    expect(screen.getByRole('button', { name: /delete action/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /keep and close dialog/i })).toBeInTheDocument();
  });

  it('shows loading state on confirm button', () => {
    renderWithProviders(
      <ConfirmDialog {...defaultProps} loading={true} />
    );
    
    const confirmButton = screen.getByRole('button', { name: /confirm action/i });
    expect(confirmButton).toHaveAttribute('data-loading', 'true');
  });

  it('disables cancel button when loading', () => {
    renderWithProviders(
      <ConfirmDialog {...defaultProps} loading={true} />
    );
    
    const cancelButton = screen.getByRole('button', { name: /cancel and close dialog/i });
    expect(cancelButton).toBeDisabled();
  });

  it('supports different variants', () => {
    const { rerender } = renderWithProviders(
      <ConfirmDialog {...defaultProps} variant="danger" />
    );
    
    let confirmButton = screen.getByRole('button', { name: /confirm action/i });
    expect(confirmButton).toBeInTheDocument();
    
    rerender(
      <MantineProvider>
        <ConfirmDialog {...defaultProps} variant="warning" />
      </MantineProvider>
    );
    
    confirmButton = screen.getByRole('button', { name: /confirm action/i });
    expect(confirmButton).toBeInTheDocument();
    
    rerender(
      <MantineProvider>
        <ConfirmDialog {...defaultProps} variant="info" />
      </MantineProvider>
    );
    
    confirmButton = screen.getByRole('button', { name: /confirm action/i });
    expect(confirmButton).toBeInTheDocument();
  });

  it('is accessible', () => {
    renderWithProviders(<ConfirmDialog {...defaultProps} />);
    
    // Modal should have accessible title
    expect(screen.getByText('Delete Item')).toBeInTheDocument();
    
    // Buttons should have accessible labels
    expect(screen.getByRole('button', { name: /confirm action/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /cancel and close dialog/i })).toBeInTheDocument();
  });
});
