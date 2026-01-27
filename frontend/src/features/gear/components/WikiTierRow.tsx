import { Group, Badge, Image, Text, Anchor, Stack, Box } from '@mantine/core';
import type { TierGroup } from '../utils/wikiGearHelpers';
import { formatPrice, getTierColor } from '../utils/wikiGearHelpers';

interface WikiTierRowProps {
  tier: TierGroup;
}

export function WikiTierRow({ tier }: WikiTierRowProps) {
  return (
    <Group key={tier.tier} wrap="nowrap" align="flex-start" gap="md">
      {/* Tier Label */}
      <Badge 
        variant="filled" 
        color={getTierColor(tier.tier)}
        w={100}
        size="md"
        style={{ flexShrink: 0 }}
      >
        {tier.tier}
      </Badge>

      {/* Items in this tier */}
      <Group gap="xs" style={{ flex: 1, flexWrap: 'wrap' }}>
        {tier.items.map((item) => (
          <Group 
            key={item.name} 
            gap={6} 
            p={6} 
            bg="white"
            style={{ 
              border: '1px solid #e0e0e0', 
              borderRadius: 6,
              boxShadow: '0 1px 2px rgba(0,0,0,0.05)',
              transition: 'all 0.2s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.1)';
              e.currentTarget.style.transform = 'translateY(-2px)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.boxShadow = '0 1px 2px rgba(0,0,0,0.05)';
              e.currentTarget.style.transform = 'translateY(0)';
            }}
          >
            {item.icon ? (
              <Image 
                src={item.icon} 
                w={32} 
                h={32} 
                fit="contain"
                fallbackSrc="https://placehold.co/32?text=?"
              />
            ) : (
              <Box w={32} h={32} bg="gray.2" style={{ borderRadius: 4 }} />
            )}
            <Stack gap={0} style={{ minWidth: 0 }}>
              <Anchor 
                href={item.wiki_url} 
                target="_blank" 
                rel="noopener noreferrer"
                size="sm" 
                fw={600} 
                c="dark" 
                underline="hover"
                style={{ 
                  textDecoration: 'none',
                  whiteSpace: 'nowrap',
                  overflow: 'hidden',
                  textOverflow: 'ellipsis',
                  maxWidth: '200px'
                }}
              >
                {item.name}
              </Anchor>
              <Text 
                size="xs" 
                c={item.price && item.price > 0 ? "dimmed" : "orange"}
                fw={500}
              >
                {formatPrice(item.price)}
              </Text>
            </Stack>
          </Group>
        ))}
      </Group>
    </Group>
  );
}
