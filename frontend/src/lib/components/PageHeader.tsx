/**
 * Consistent page header with breadcrumbs
 */
import { Group, Title, Breadcrumbs, Anchor, Box } from '@mantine/core';
import { ReactNode } from 'react';

export interface Breadcrumb {
  /** Breadcrumb label */
  label: string;
  /** Optional href for navigation */
  href?: string;
  /** Optional click handler */
  onClick?: () => void;
}

export interface PageHeaderProps {
  /** Page title */
  title: string;
  /** Optional breadcrumbs */
  breadcrumbs?: Breadcrumb[];
  /** Optional action buttons */
  actions?: ReactNode;
  /** Optional subtitle/description */
  subtitle?: string;
}

/**
 * PageHeader provides consistent page titles with optional breadcrumbs and actions.
 *
 * @example
 * ```tsx
 * <PageHeader
 *   title="Flip Scanner"
 *   breadcrumbs={[
 *     { label: 'Home', onClick: () => navigate('/') },
 *     { label: 'Flipping', onClick: () => navigate('/flipping') },
 *     { label: 'Scanner' }
 *   ]}
 *   actions={<Button>Refresh</Button>}
 *   subtitle="Find profitable flip opportunities"
 * />
 * ```
 */
export function PageHeader({
  title,
  breadcrumbs,
  actions,
  subtitle,
}: PageHeaderProps) {
  return (
    <Box mb="xl">
      {breadcrumbs && breadcrumbs.length > 0 && (
        <Breadcrumbs mb="xs" aria-label="Breadcrumb navigation">
          {breadcrumbs.map((crumb, index) => {
            const isLast = index === breadcrumbs.length - 1;

            if (isLast) {
              return (
                <Anchor
                  key={index}
                  component="span"
                  c="dimmed"
                  aria-current="page"
                >
                  {crumb.label}
                </Anchor>
              );
            }

            return (
              <Anchor
                key={index}
                href={crumb.href}
                onClick={(e) => {
                  if (crumb.onClick) {
                    e.preventDefault();
                    crumb.onClick();
                  }
                }}
                aria-label={`Navigate to ${crumb.label}`}
              >
                {crumb.label}
              </Anchor>
            );
          })}
        </Breadcrumbs>
      )}

      <Group justify="space-between" align="flex-start" wrap="wrap">
        <Box>
          <Title order={1} size="h2" mb={subtitle ? 4 : 0}>
            {title}
          </Title>
          {subtitle && (
            <Title order={2} size="h6" fw={400} c="dimmed">
              {subtitle}
            </Title>
          )}
        </Box>

        {actions && (
          <Box style={{ flexShrink: 0 }}>
            {actions}
          </Box>
        )}
      </Group>
    </Box>
  );
}
