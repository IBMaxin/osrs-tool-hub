import { render, screen } from '@testing-library/react';
import { userEvent } from '@testing-library/user-event';
import { describe, it, expect, vi } from 'vitest';
import { MantineProvider, Button } from '@mantine/core';
import { PageHeader } from '../../lib/components/PageHeader';

const renderWithProviders = (ui: React.ReactElement) => {
  return render(<MantineProvider>{ui}</MantineProvider>);
};

describe('PageHeader', () => {
  it('renders title', () => {
    renderWithProviders(<PageHeader title="Test Page" />);
    expect(screen.getByRole('heading', { name: 'Test Page' })).toBeInTheDocument();
  });

  it('renders subtitle when provided', () => {
    renderWithProviders(
      <PageHeader title="Test Page" subtitle="Page description" />
    );
    expect(screen.getByText('Page description')).toBeInTheDocument();
  });

  it('renders breadcrumbs when provided', () => {
    renderWithProviders(
      <PageHeader
        title="Test Page"
        breadcrumbs={[
          { label: 'Home', onClick: vi.fn() },
          { label: 'Section', onClick: vi.fn() },
          { label: 'Current Page' },
        ]}
      />
    );

    expect(screen.getByText('Home')).toBeInTheDocument();
    expect(screen.getByText('Section')).toBeInTheDocument();
    expect(screen.getByText('Current Page')).toBeInTheDocument();
  });

  it('last breadcrumb has aria-current', () => {
    renderWithProviders(
      <PageHeader
        title="Test Page"
        breadcrumbs={[
          { label: 'Home' },
          { label: 'Current' },
        ]}
      />
    );

    const currentCrumb = screen.getByText('Current');
    expect(currentCrumb).toHaveAttribute('aria-current', 'page');
  });

  it('calls onClick when breadcrumb is clicked', async () => {
    const user = userEvent.setup();
    const onClick = vi.fn();

    renderWithProviders(
      <PageHeader
        title="Test Page"
        breadcrumbs={[
          { label: 'Home', onClick },
          { label: 'Current' },
        ]}
      />
    );

    await user.click(screen.getByText('Home'));
    expect(onClick).toHaveBeenCalledTimes(1);
  });

  it('renders action buttons', () => {
    renderWithProviders(
      <PageHeader
        title="Test Page"
        actions={<Button>Action</Button>}
      />
    );

    expect(screen.getByRole('button', { name: 'Action' })).toBeInTheDocument();
  });
});
