import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { MantineProvider } from '@mantine/core';
import { IconCoins } from '@tabler/icons-react';
import { EmptyState } from '../../lib/components/EmptyState';

const renderWithProviders = (ui: React.ReactElement) => {
  return render(<MantineProvider>{ui}</MantineProvider>);
};

describe('EmptyState', () => {
  const defaultProps = {
    icon: <IconCoins size={48} data-testid="icon" />,
    title: 'No data found',
    description: 'Try adjusting your filters',
  };

  it('renders icon, title, and description', () => {
    renderWithProviders(<EmptyState {...defaultProps} />);

    expect(screen.getByTestId('icon')).toBeInTheDocument();
    expect(screen.getByText('No data found')).toBeInTheDocument();
    expect(screen.getByText('Try adjusting your filters')).toBeInTheDocument();
  });

  it('icon has aria-hidden for accessibility', () => {
    renderWithProviders(<EmptyState {...defaultProps} />);

    const iconContainer = screen.getByTestId('icon').closest('[aria-hidden]');
    expect(iconContainer).toHaveAttribute('aria-hidden', 'true');
  });

  it('renders action button when provided', () => {
    renderWithProviders(
      <EmptyState
        {...defaultProps}
        action={{
          label: 'Reset Filters',
          onClick: vi.fn(),
        }}
      />
    );

    expect(screen.getByRole('button', { name: 'Reset Filters' })).toBeInTheDocument();
  });

  it('calls action onClick when button is clicked', async () => {
    const user = userEvent.setup();
    const onClick = vi.fn();

    renderWithProviders(
      <EmptyState
        {...defaultProps}
        action={{
          label: 'Reset Filters',
          onClick,
        }}
      />
    );

    const button = screen.getByRole('button', { name: 'Reset Filters' });
    await user.click(button);

    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('does not render action button when not provided', () => {
    renderWithProviders(<EmptyState {...defaultProps} />);

    expect(screen.queryByRole('button')).not.toBeInTheDocument();
  });

  it('supports different sizes', () => {
    const { rerender } = renderWithProviders(<EmptyState {...defaultProps} size="sm" />);

    expect(screen.getByText('No data found')).toBeInTheDocument();

    rerender(
      <MantineProvider>
        <EmptyState {...defaultProps} size="lg" />
      </MantineProvider>
    );

    expect(screen.getByText('No data found')).toBeInTheDocument();
  });

  it('has accessible button label', () => {
    renderWithProviders(
      <EmptyState
        {...defaultProps}
        action={{
          label: 'Do Something',
          onClick: vi.fn(),
        }}
      />
    );

    const button = screen.getByRole('button', { name: 'Do Something' });
    expect(button).toHaveAccessibleName('Do Something');
  });
});
